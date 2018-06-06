"""
    Project Name    :   Colorful Memories-Auto Colorization
    Function Name   :   auto_colorization.py code
    Authors         :   Kallakuri Prabhakar(903094733) , Daniel Smith(901636936)
    Date            :   07/15/2016
"""

import numpy as np
import cv2
import sys
import os
import string
import gif_util as gu      #tools for decomposign and making gifs
import warnings
import re
import imghdr

warnings.filterwarnings("ignore", category=FutureWarning)


# This code does color to gray scale mapping or creates a translation map of an image
def color_gray_map(color):

        # The code below does auto colorization of gray scale image to a
        # a color image. This code was built as part of CS6475 Computational Photography
        # summer project

  grey=cv2.cvtColor(color, cv2.COLOR_BGR2GRAY)
  gray_to_color_map = [None]*256
  new_values = np.zeros(256)

  for i in range(grey.shape[0]):
    for j in range(grey.shape[1]):
      # gray_value contains gray pixel value . Its a single pixel channel value  from 0 - 255
      gray_value = grey[i][j]
      if gray_value < 0:
        print "Pixel value is below  0:  ", gray_value
        gray_value = 0
      elif gray_value > 255:
        print "Pixel value is greater than 255:  ", gray_value
        gray_value = 255
      # color_value contains color pixel value . Its a 3 channel value from 0 - 255
      color_value = color[i][j]
      if gray_to_color_map[gray_value] == None:
        gray_to_color_map[gray_value] = color[i][j] *1.0
        new_values[gray_value] = 0
      else:
          gray_to_color_map[gray_value]+=color[i][j]
      # Arrays that stores the Index
      new_values[gray_value]+=1

  # We do the average pixel calculation in this block of code
  for i in range(256):
    if new_values[i]>1:
      if gray_to_color_map[i] == None:
        gray_to_color_map[i] = np.ones(3, float)
      else:
        gray_to_color_map[i] = gray_to_color_map[i]/(new_values[i])

  return gray_to_color_map


def apply_gray2color_map(image, map):

# Create a  colorized_image with the same size that of gray scale .
# The only difference will be the number of channel

  colorized_image = np.zeros((image.shape[0], image.shape[1], 3), int )
  for i in range(image.shape[0]):
    for j in range(image.shape[1]):
      gray_value = image[i][j]
      while gray_value < 256 and map[gray_value] == None:
        gray_value+=1

      # If there is a value found for the gray pixel in the color map , then apply the transformation
      # from map to this gray pixel value. This process is crucial as we are colorizing the pixel value in gray image
      # and making it a color image. There are challenges in doing this and we discussed in detail on the final
      # project presentation.

      if map[image[i][j]] != None:
        colorized_image[i][j] = map[image[i][j]]
      else:
        colorized_image[i][j] = np.ones(3)*image[i][j]

  return colorized_image

if __name__ == '__main__':
    if len( sys.argv ) < 3:
      print "Please supply 2 arguments: color image and gray image to colorize"
      sys.exit( 1 )

    color_sample = sys.argv[1]
    # Read the sample color image
    color_sample_image = cv2.imread(color_sample)

    # This calls the critical function - auto colorization code that generates color-gray mapping
    gray_to_color_map = color_gray_map(color_sample_image)
    converted_images = []

    # If directory of input images is given for gif creation.
    # Pass the command line arguments with proper directory structure for  color and gray scale image.

    if os.path.isdir(sys.argv[2]):
        for filename in os.listdir(sys.argv[2]):
          grayscale_sample_image=cv2.imread(os.path.join(sys.argv[2],filename))
          print os.path.join(sys.argv[2],filename)

        # Convert the image to gray scale
          grayscale_sample_image=cv2.cvtColor(grayscale_sample_image, cv2.COLOR_BGR2GRAY)
          colorized = apply_gray2color_map(grayscale_sample_image, gray_to_color_map)
          ctarget = os.path.join(sys.argv[3],"colorized"+filename)
          cv2.imwrite(ctarget, colorized)
          converted_images.append(ctarget)
        # Code to create GIF from set of images
        gu.build_gif(converted_images, os.path.join(sys.argv[3],"convertedgif.gif"))

        # Save the GIF at specific location
        print "gif built at "+ os.path.join(sys.argv[3],"convertedgif.gif")

    # This code checks if the input parameter passed is a file instead of directory
    elif os.path.isfile(sys.argv[2]):
        # If provided file is a gif
        if imghdr.what(sys.argv[2])=='gif':
            files = gu.gif_2_images(sys.argv[2])
            for filename in files:
              grayscale_sample_image = cv2.imread(filename)

              # Convert the image to gray scale
              grayscale_sample_image = cv2.cvtColor(grayscale_sample_image, cv2.COLOR_BGR2GRAY)

              # Call the autocolorization code to colorize the image
              colorized = apply_gray2color_map(grayscale_sample_image, gray_to_color_map)
              ctarget = os.path.join(sys.argv[3],filename)
              cv2.imwrite(ctarget.replace("gif_storage",""), colorized)
              converted_images.append(ctarget.replace("gif_storage",""))

            gu.build_gif(converted_images, os.path.join(sys.argv[3],"convertedgif.gif"))
            print "gif built at "+ os.path.join(sys.argv[3],"convertedgif.gif")
        else:
            if sys.argv[3] != None:
                #Saving the color image with .PNG extension
                ctarget = sys.argv[3] + ".png"
            print "Dealing with a file"
            grayscale_sample_image=cv2.imread(sys.argv[2])
            print sys.argv[2]

            # Convert to grayscale.
            grayscale_sample_image=cv2.cvtColor(grayscale_sample_image, cv2.COLOR_BGR2GRAY)
            colorized = apply_gray2color_map(grayscale_sample_image, gray_to_color_map)
            cv2.imwrite(ctarget, colorized)

    else:
        print "Please provide valid file or file path as input parameter"
    sys.exit(0)
