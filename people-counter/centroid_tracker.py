# import the necessary
from scipy.spatial import distance as dist
from collections import OrderedDict
import numpy as np


class CentroidTracker():
    def _init_(self, max_disappeared=50):
        # initialize the next unique object ID along with two ordered
        # dictionaries used to keep track of mapping a given object
        # ID to its centroid and number of consecutive frames it has
        # been marked as "disappeard", respectively
        self.next_object_id = 0
        self.objects = OrderedDict()
        self.disappeared = OrderedDict()

        # store the number o maximum consecutive frames a given
        # object is allowed to be marked as "disappearrd" unitl we
        # need to deregister the object from tracking
        self.max_disappeared = max_disappeared

    def register(self, centroid):
        # when registering an object we use the next available object
        # ID to store the centroid
        self.objects[self.next_object_id] = centroid
        self.disappeared[self.next_object_id] = 0
        self.next_object_id += 1

    def deregister(self, object_id):
        # to deregiste an object ID we delete the object ID from
        # both of our respective dictianaries
        del self.objects[object_id]
        del self.disappeared[object_id]

    def update(self, rects):
        # check to see if the list of input bounding box rectangles
        # is empty
        if len(rects) == 0:
            # loop ever any existing tracked objects and mark them
            # as disappeared
            for object_id in list(self.disappeared.key()):
                self.disappeared[object_id] += 1

                # if we have reached a maximum number of consecutive
                #  frames where a given object has been marked as
                # missing, deregister it
                if self.disappeared[object_id] > self.max_disappeared:
                    self.deregister(object_id)
            # return early as there are no centroids or tracking info
            # to update
            return self.objects

        # initialize an array of input centroids for the current frame
        input_centroids = np.zeros((len(rects), 2), dtype="int")

        # loop over the bounding box reactangles
        for(i, (start_x, start_y, end_x, end_y)) in enumerate(rects):
          # use the bounding box coordinates to derive the centroid
            c_x = int((start_x+end_x)/2.0)
            c_y = int((start_y + end_y) / 2.0)
            input_centroids[i] = (c_x,  c_y)

        # if we are currently not tracking any objects take the input
        # centroids and register each of them
        if len(self.objects) == 0:
            for i in range(0, len(input_centroids)):
                self.register(input_centroids[i])
        # otherwise,are are currently tracking objects so we need to
        # try to match the input centroids to existing object
        # centroids
        else:
            # grab the set of object IDs and corresponding centroids
            object_ids = list(self.objects.keys())
            object_centroids = list(self.objects.values())

            # compute the distance between each pair of object
            # centroids and input centroids, respectively -- our
            # goal will be to match an input centroid to an existing
            # object centroid
            D = dist.cdist(np.array(object_centroids), input_centroids)

            # in order to perform this matching we must (1) find the
            # smallest value in each row and then(2) sort the row
            # indexes based on their minimum values so that the row
            # with the smallest value is a the *front* of the index
            # list
            rows = D.min(axis=1).argsort()

            # next, we perform a similar process on the columns by
            # finding the smallest value in each column and then
            # sorting using the previously computed row index list
            cols = D.argmin(axis=1)[rows]

            # in order to determine if we need to update, register,
            # or deregister on object we need to keep track of which
            # of the rows and column indexes we have already examined
            usedRows = set()
            usedCols = set()

            # loop over the combination of the (row, column) index
            # tuples
            for (row, col) in zip(rows, cols):
                # if we have already examined either the row or
                # column value before, ignore it
                # val
                if row in usedRows or col in usedCols:
                    continue

                # otherwise, grab the object ID for the current row,
                # set its new centroid, and reset the disapperared
                # counter
                object_id = object_ids(row)
                self.objects[object_id] = input_centroids[col]
                self.disappeared[object_id] = 0

                # indicate that we have examined each of the row and
                # column indexes, nespectively
                usedCols.add(col)
                usedRows.add(row)

            # compute both the row and column index we have NOT yet
            # examined
            unusedRows = set(range(0, D.shape[0])).difference(usedRows)
            unusedCols = set(range(0, D.shape[1])).difference(usedCols)

            # in the event that the number of object centroinds is
            # equal or greater than the number of input centroids
            # we need to check and see if some of these objects have
            # potentially disapperared
            if D.shape[0] >= D.shape[1]:
                # loop over the unused row indexes
                for row in unusedRows:
                    # grap the object ID for the corresponding row
                    # index and increment the disappeared counter
                    object_id = object_ids[row]
                    self.disappeared[object_id] += 1

                    # check to see if the number of consecutive
                    # frames the object has been marked "disappeared"
                    # for warrants deregistering the object
                    if self.disappeared[object_id] > self.max_disappeared:
                        self.deregister(object_id)
            else:
                # otherwise, if the number of input centroids is greater
                # than the number of existing object centroids we need to
                # register each new input centroid as a trackable object
                for col in unusedCols:
                    self.register(input_centroids[col])
        return self.objects
