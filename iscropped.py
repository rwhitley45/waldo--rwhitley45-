# Author: Ryan Whitley <rwhitley45@gmail.com>
"""Cropped image determination

This program compares two images and determines if one image is cropped 
from the other. If so, it returns the top-left coordinates of the cropped image
within the original image:

The module contains the following functions:

    - iscropped -- Scans the larger image row wise until pixel value matches 
        the first pixel value of the smaller image. If none exists, we return
        that the smaller image is not cropped from the other.

    - checkpotential -- Starting at some coordinates x,y in the larger image,
        determines if the smaller image is cropped from the larger by comparing
        each pixel in the cooresponding sub-image. Returns True if so.

    - iscroppedjpg -- Similar to iscropped, but we say a pixel value mathes if
        it's within some standard deviation of smaller images pixel value. This
        is due to the lossy format of JPEGs. At standard deviation of 20 is chosen

    - checkpotentialjpg -- Similar to checkpotential, except we are once again
        comparing within some standard deviation of the smaller images pixel 
        value.

Usage:
    python iscropped.py imagefolder/image.ext imgfolder/image2.ext
"""

import cv2
import sys
import os.path
#import numpy as np

def iscropped(img, imgc):
    for x in range(0, img.shape[0]):
        for y in range(0, img.shape[1]):
            if img[x][y] == imgc[0][0]:
                check = checkpotential(img, imgc, x, y)
                if check == True:
                    return "Top-left coordinates: "+str(y)+","+str(x)
    return "Image is not cropped from the other"


def checkpotential(img, imgc, sx, sy):
    #test = np.zeros((imgc.shape[0],imgc.shape[1]))
    ex = sx+imgc.shape[0]
    ey = sy+imgc.shape[1]
    if ex > img.shape[0] or ey > img.shape[1]: #will sub-image run out of bounds?
        return False
    px = -1
    for x in range(sx, ex):
        px += 1
        py = 0
        for y in range(sy, ey):
            #test[px][py] = img[x][y]
            if img[x][y] != imgc[px][py]:
                return False
            py += 1
    # cv2.imwrite("test.jpg",test)
    return True

def iscroppedjpg(img, imgc):
    stdvh = imgc[0][0] + 20
    stdvl = imgc[0][0] - 20
    for x in range(0, img.shape[0]):
        for y in range(0, img.shape[1]):
            if img[x][y] >= stdvl and img[x][y] <= stdvh:
                check = checkpotentialjpg(img, imgc, x, y)
                if check == True:
                    return "Top-left coordinates: "+str(y)+","+str(x)
    return "Image is not cropped from the other"


def checkpotentialjpg(img, imgc, sx, sy):
    #test = np.zeros((imgc.shape[0],imgc.shape[1]))
    ex = sx+imgc.shape[0]
    ey = sy+imgc.shape[1]
    if ex > img.shape[0] or ey > img.shape[1]: #will sub-image run out of bounds?
        return False
    px = -1
    for x in range(sx, ex):
        px += 1
        py = 0
        for y in range(sy, ey):
            #test[px][py] = img[x][y]
            stdvh = imgc[px][py] + 20
            stdvl = imgc[px][py] - 20
            if img[x][y] < stdvl or img[x][y] > stdvh:
                return False
            py += 1
    # cv2.imwrite("test.jpg",test)
    return True

img1 = cv2.imread(sys.argv[1], 0)
img2 = cv2.imread(sys.argv[2], 0)

ext = os.path.splitext(sys.argv[1])[1] # grab image extension

if img1.shape[0] == img2.shape[0] and img1.shape[1] == img2.shape[1]:
    print("Images are the same size")
elif img2.shape[0] <= img1.shape[0] and img2.shape[1] <= img1.shape[1]: #img1 > img2?
    if(ext.lower() == '.jpg' or ext.lower() == '.jpeg'):
        print(iscroppedjpg(img1, img2))
    else:
        print(iscropped(img1, img2))
elif img1.shape[0] <= img2.shape[0] and img1.shape[1] <= img2.shape[1]: #img2 > img1?
    if(ext.lower() == '.jpg' or ext.lower() == '.jpeg'):
        print(iscroppedjpg(img2, img1))
    else:
        print(iscropped(img2, img1))
else:
    print("Dimension mismatch in X or Y")  
