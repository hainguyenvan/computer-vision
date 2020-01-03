import glob
import os
import sys
from PIL import Image

size = 480, 680

# for infile in sys.argv[1:]:
infile = "/home/user1/Desktop/images"
outfile = "/home/user1/Desktop/resize"
for pathAndFilename in glob.iglob(os.path.join(infile, "*")):
    title, ext = os.path.splitext(os.path.basename(pathAndFilename))
    filename = title+ext
    input = infile+'/'+filename
    output = outfile + "/" + filename
    im = Image.open(input)
    im.thumbnail(size, Image.ANTIALIAS)
    im.save(output)