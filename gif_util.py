"""
    Project Name    :   Colorful Memories-Auto Colorization
    Function Name   :   color_util.py code
    Authors         :   Kallakuri Prabhakar(903094733) , Daniel Smith(901636936)
    Date            :   07/15/2016
"""

import numpy as np
import scipy
import cv2
from images2gif import writeGif
from PIL import Image
import os


# Creates a GIF image from set of images from input folder
def build_gif(images, filename):
    files = []
    for file in images:
        meh = Image.open(file)
        files.append(meh)
    # writeGIF is a function that creates GIF and is a part of images2gif library
    # print writeGif.__doc__
    # Above print statement would give you details about the function in detail
    writeGif(filename, files, duration=0.2)

# Creates images  from GIF image
def gif_2_images(file):
    files = []
    i = 0
    im = Image.open(file)    
    if not os.path.exists("gif_storage"):
        os.makedirs("gif_storage")
    try:
        while 1:
            im2 = im.convert('RGBA')
            im2.load()
            background = Image.new("RGB", im2.size, (255, 255, 255))
            background.paste(im2, mask = im2.split()[3] )
            background.save('gif_storage\\colorized'+str(i)+'.jpg', 'JPEG', quality=80)
            files.append('gif_storage\\colorized'+str(i)+'.jpg')
            i += 1
            im.seek( im.tell() + 1 )
    except EOFError:
       pass
    return files

