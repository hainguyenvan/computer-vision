# import the necessary package
from centroid_tracker import CentroidTracker
from trackable_object import TracableObject
from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np
import imutils
import time
import dlib
import cv2

# construct the argument parse and parse the argument
prototxt = "mobilenet_ssd/MobileNetSSD_deploy.prototxt"
model = "mobilenet_ssd/MobileNetSSD_deploy.caffemodel"
input_video = "videos/example_01.mp4"
output_video = "ouput/example_01.mjpg"
confidence_target = 0.4
skip_frame = 30

CLASSES = ["background", "aeroplane", "bicycle",
           "bird", "boat", "bottle", "bus", "car", "cat", "chair", "cow", "diningtable", "dog", "horse", "motorbike", "person", "pottedplant", "sheep", "sofa", "train", "tvmonitor"]
# load our serialized model from disk
print("[INFO] loading model ...")
net = cv2.dnn.readNetFromCaffe(prototxt, model)

# if a video path was not supplied, grad a reference to the webcam
print("[Info] opening video file ...")
vs = cv2.VideoCapture(input_video)

# initialize the video writer (we'll instantiate later if need be)
writer = None

# initialize the frame dimensions (we'll set them as soon as we read)
# the first frame from the video)
w = None
h = None

# instantiate our centroid tracker, then initialize a list to store
# each of our dlib correlation, trackers, followed by a dictionary to
# map each unique object ID to a TrackableObject
ct = CentroidTracker()
trackers = []
trackable_objects = {}

# initialize the total number of frames processed thus far, along
# with the total number of objects that have moved either up or down
total_frames = 0
total_down = 0
total_up = 0

# start the frames per second
fps = FPS().start()

# loop over frames from the video stream
while True:
    # grab the next frame and handle if we are reading from either
    # VideoCapture or VideoStream
    ret, frame = vs.read()
    if frame is None:
        break

    # resize the frame to have a maximum width of 500 pixels (the
    # less data we have, the faster we can process it), then convert
    # the frame from BGR to RGB for dlib
    frame = imutils.resize(frame, width=500)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # if the frame dimensions are empty, set them
    if w is None or h is None:
        (w, h) = frame.shape[:2]

    # if we are supposed to be writing a video to disk, initialize
    # the writer
    # if output_video is not None and writer is None:
    #     fourcc = cv2.VideoWriter_fourcc(*"MJPG")
    #     writer = cv2.VideoWriter(output_video, fourcc, 30, (w, h), True)

    # initialize the current status along with our list of bounding
    # box reactangles returned by ether(1) our object detector or
    # (2) the correlation trackers
    status = "Waiting"
    rects = []

    # check to see if we should run a more computationlly expensive
    # object detection method to aid our tracker
    if total_frames % skip_frame == 0:
        status = "Detecting"
        trackers = []

        # convert the frame to a blob and pass the blob through the
        # network and obtain the detections
        blob = cv2.dnn.blobFromImage(frame, 0.007843, (w, h), 127.5)
        net.setInput(blob)
        detections = net.forward()

        # loop over the detections
        for i in np.arange(0, detections.shape[2]):
            # extract the confidence
            # with the prediction
            confidence = detections[0, 0, i, 2]

            # filter out weak detections by requirting a minimum
            # confidence
            if confidence > confidence_target:
                # extract the index of the class label from the
                # detections list
                idx = int(detections[0, 0, i, 1])

                # if the class label is not a person, ignore it
                if CLASSES[idx] != "person":
                    continue

                # compute the(x,y)-coordinates of the bounding box
                # for the objects
                box = detections[0, 0, i, 3:7]*np.array([w, h, w, h])
                (start_x, start_y, end_x, end_y) = box.astype("int")

                # construct a dlib rectangle object from the bounding
                # box coordinates and then start the dlib correlation
                # tracker
                tracker = dlib.correlation_tracker()
                rect = dlib.rectangle(start_x, start_y, end_x, end_y)
                tracker.start_track(rgb, rect)

                # add the tracker to our list of trackers so we can
                # utilize it during skip frames
                trackers.append(tracker)

            else:
                # loop over the trackers
                for traker in trackers:
                    # set the status of our system to be "tracking" rather
                    # than "waiting" or "detecting"
                    status = "Tracking"
                    tracker.update(rgb)
                    pos = tracker.get_position()

                    # unpack the position object
                    start_x = int(pos.left())
                    start_y = int(pos.top())
                    end_x = int(pos.right())
                    end_y = int(pos.bottom())
                    rects.append((start_x, start_y, end_x, end_y))

    # use the centroid tracker to associate the (1) old object
    # centroids with (2) the newly computed object centroids
    objects = ct.update(rects)

    # loop over the tracked objects
    for (object_id, centroid) in objects.items():
        # check to see if a trackable object exists for the current
        # object ID
        to = trackable_objects.get(object_id, None)

        # if there is no existing trackable object, create one
        if to is None:
            to = TracableObject(object_id, centroid)
        else:
            y = [c[1] for c in to.centroids]
            direction = centroid[i] - np.mean(y)
            to.centroids.append(centroid)

            if not to.counted:
                if direction < 0 and centroid[1] < h//2:
                    total_up += 1
                    to.counted = True
                elif direction > 0 and centroid[1] > h//2:
                    total_down += 1
                    to.counted = True
        trackable_objects[object_id] = to

    # show frame
    cv2.imshow("frame", frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break
