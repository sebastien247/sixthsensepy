#!/usr/bin/python

# Standard imports
import cv2
import numpy as np;
from PIL import Image


def getDetector(type="ORB"):
    detector = None
    if(type=="BRISK"):
        detector = cv2.FeatureDetector_create("BRISK")
    if(type=="Dense"):
        detector = cv2.FeatureDetector_create("Dense")
    if(type=="FAST"):
        detector = cv2.FeatureDetector_create("FAST")
    if(type=="GFTT"):
        detector = cv2.FeatureDetector_create("GFTT")
    if(type=="HARRIS"):
        detector = cv2.FeatureDetector_create("HARRIS")
    if(type=="MSER"):
        detector = cv2.FeatureDetector_create("MSER")
    if(type=="ORB"):
        detector = cv2.FeatureDetector_create("ORB")
    if(type=="SIFT"):
        detector = cv2.FeatureDetector_create("SIFT")
    if(type=="STAR"):
        detector = cv2.FeatureDetector_create("STAR")
    if(type=="SURF"):
        detector = cv2.FeatureDetector_create("SURF")
    if(type=="SimpleBlob"):#NO funca
        detector = cv2.SimpleBlobDetector()

    return detector

def RGB2HSV(R,G,B):
    RGB = np.uint8([[[R,G,B ]]])
    HSV = cv2.cvtColor(RGB,cv2.COLOR_BGR2HSV)
    return HSV

def keypoints_size(p):
    return p.size


red_hsv = RGB2HSV(255,0,0)
green_hsv = RGB2HSV(0,255,0)
blue_hsv = RGB2HSV(0,0,255)

print red_hsv
print green_hsv
print blue_hsv

############################################

# Setup SimpleBlobDetector parameters.
params = cv2.SimpleBlobDetector_Params()

# Change thresholds
params.minThreshold = 10
params.maxThreshold = 200

# Filter by Color.
# params.filterByColor = True
# params.blobColor = 0

# Filter by Area.
params.filterByArea = True
params.minArea = 1000
params.maxArea = 8000

# Filter by Circularity
params.filterByCircularity = True
params.minCircularity = 0.1

# Filter by Convexity
params.filterByConvexity = True
params.minConvexity = 0

# Filter by Inertia
params.filterByInertia = True
params.minInertiaRatio = 0.01

# Create a detector with the parameters
ver = (cv2.__version__).split('.')
if int(ver[0]) < 3 :
    detector = cv2.SimpleBlobDetector(params)
else : 
    detector = cv2.SimpleBlobDetector_create(params)

############################################


# ---------- Red Mask ---------- #
#- lower mask (0-10)
l_lower_red = np.array([0,125,125])
l_upper_red = np.array([10,255,255])
#- upper mask (170-180)
u_lower_red = np.array([170,125,125])
u_upper_red = np.array([180,255,255])
# -------- End Red Mask -------- #

# ---------- Green Mask ---------- #
#- mask
l_lower_green = np.array([60,90,30])
l_upper_green = np.array([100,255,255])
# -------- End Green Mask -------- #

# ---------- Blue Mask ---------- #
#- mask
l_lower_blue = np.array([100,130,130])
l_upper_blue = np.array([120,255,255])
# -------- End Blue Mask -------- #

# ---------- Yellow Mask ---------- #
#- mask
l_lower_yellow = np.array([22,130,130])
l_upper_yellow = np.array([30,255,255])
# -------- End Yellow Mask -------- #


cam = cv2.VideoCapture(0)
while 1:
    keypoints = []
    _, im = cam.read()

    # # Convert to HSV
    im_hsv=cv2.cvtColor(im, cv2.COLOR_BGR2HSV)

    #- Masks
    red_mask_lower = cv2.inRange(im_hsv, l_lower_red, l_upper_red)
    red_mask_upper = cv2.inRange(im_hsv, u_lower_red, u_upper_red)
    red_mask = 255 - (red_mask_lower + red_mask_upper)

    green_mask_lower = cv2.inRange(im_hsv, l_lower_green, l_upper_green)
    green_mask = 255 - green_mask_lower

    blue_mask_lower = cv2.inRange(im_hsv, l_lower_blue, l_upper_blue)
    blue_mask = 255 - blue_mask_lower

    yellow_mask_lower = cv2.inRange(im_hsv, l_lower_yellow, l_upper_yellow)
    yellow_mask = 255 - yellow_mask_lower

    # Detect blobs.
    keypoints_r = detector.detect(red_mask)
    keypoints_g = detector.detect(green_mask)
    keypoints_b = detector.detect(blue_mask)
    keypoints_y = detector.detect(yellow_mask)

    # Get upper size of keypoints
    if keypoints_r:
        keypoints.append(max(keypoints_r, key=keypoints_size))
    if keypoints_g:
        keypoints.append(max(keypoints_g, key=keypoints_size))
    if keypoints_b:
        keypoints.append(max(keypoints_b, key=keypoints_size))
    if keypoints_y:
        keypoints.append(max(keypoints_y, key=keypoints_size))


    # Draw detected blobs as red circles. cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob
    im_with_keypoints = cv2.drawKeypoints(im, keypoints, np.array([]), (0,255,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    # Show blobs
    cv2.imshow("im", im_with_keypoints)
    cv2.imshow("red_mask", red_mask)
    cv2.imshow("green_mask", green_mask)
    cv2.imshow("blue_mask", blue_mask)
    cv2.imshow("yellow_mask", yellow_mask)
    cv2.waitKey(1)