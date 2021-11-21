#!/usr/bin/env python

import cv2
import numpy as np
import math

# ========================= Student's code starts here =========================

# Params for camera calibration
# theta = -.006435106
# beta = 7.663
# tx = 15.466928640101
# ty = -0.39731150456015

# theta = -0.09
# beta = 7.300
# tx=29.7435628054
# ty=7.63807206584

theta = -0.09
beta = 7.300
tx=28.9435628054
ty=10.33807206584

# Function that converts image coord to world coord
# Note: input x corresponds to columns in the image, input y is rows in the image
def IMG2W(x,y):
    
    # xc = (blob_image_center[0][1]-240)/beta
    # yc = (blob_image_center[0][0]-320)/beta

    xc = (y-240)/beta
    yc = (x-320)/beta
    
    xw = xc*math.cos(theta) - yc*math.sin(theta) + tx
    xw *= 10
    yw = xc*math.sin(theta) + yc*math.cos(theta) + ty
    yw *= 10
    zw = 30

    # xw = (y-240)/beta
    # yw = (x-320)/beta
    # zw = 15

    return (xw,yw,zw)

# ========================= Student's code ends here ===========================

def blob_search(image_raw, color):

    # Setup SimpleBlobDetector parameters.
    params = cv2.SimpleBlobDetector_Params()

    # ========================= Student's code starts here =========================

    # Filter by Color
    params.filterByColor = False

    # Filter by Area.
    params.filterByArea = True
    params.minArea = 200
    params.maxArea = 800

    # params.minArea = 0
    # params.maxArea = 500

    # Filter by Circularity
    # params.filterByCircularity = True
    # params.minCircularity = 0.9;

    # Filter by Inerita
    params.filterByInertia = False

    # Filter by Convexity
    params.filterByConvexity = False

    # ========================= Student's code ends here ===========================

    # Create a detector with the parameters
    detector = cv2.SimpleBlobDetector_create(params)

    # Convert the image into the HSV color space
    hsv_image = cv2.cvtColor(image_raw, cv2.COLOR_BGR2HSV)

    # ========================= Student's code starts here =========================
    # lower = (160,50,50)     # pink lower
    # upper = (179,255,255)   # pink upper

    lower = (110,50,50)     # blue lower
    upper = (130,255,255)   # blue upper
    if color == "yellow":
        lower = (10,50,50)     # yellow lower
        upper = (30,255,255)   # yellow upper
    elif color == "green":    
        lower = (53,0,0)     # green lower
        upper = (73,255,255)   # green upper
    elif color == "pink":
        lower = (150,50,50)     # pink lower
        upper = (180,255,255)   # pink upper

    # Define a mask using the lower and upper bounds of the target color
    mask_image = cv2.inRange(hsv_image, lower, upper)

    # ========================= Student's code ends here ===========================

    keypoints = detector.detect(mask_image)

    cv2.namedWindow("Camera View")
    cv2.imshow("Camera View", image_raw)
    cv2.namedWindow("Mask View")
    cv2.imshow("Mask View", mask_image)
    # cv2.namedWindow("Keypoint View")
    # cv2.imshow("Keypoint View", im_with_keypoints)

    cv2.waitKey(2)

    # Find blob centers in the image coordinates
    blob_image_center = []
    # num_blobs = len(keypoints)
    # for i in range(num_blobs):
    #     blob_image_center.append((keypoints[i].pt[0],keypoints[i].pt[1]))
    if len(keypoints) > 0:
        blob_image_center = [keypoints[0].pt[0],keypoints[0].pt[1]]
    else:
        # print("NO BLOCKS FOUND!!!")
        return None

    cpy = image_raw.copy()
    # Draw the keypoints on the detected block
    im_with_keypoints = cv2.drawKeypoints(image_raw, keypoints, cpy, color=(0,0,200), flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS) #### 

    # xw_yw_zw = []

    if(len(blob_image_center) == 0):
        print("No block found!")
        return None
    else:
        # dist = math.sqrt((blob_image_center[0][0]-blob_image_center[1][0])**2 + (blob_image_center[0][1]-blob_image_center[1][1])**2)
        # print(dist)
        # Convert image coordinates to global world coordinate using IM2W() function
        # dx = blob_image_center[0][0]-blob_image_center[1][0]
        # dy = blob_image_center[0][1]-blob_image_center[1][1]
        # print(math.atan2(dy, dx))
        # xc = (blob_image_center[0][1]-240)/beta
        # yc = (blob_image_center[0][0]-320)/beta
        # Tx = 162.5 - xc*math.cos(theta) + yc*math.sin(theta)
        # Ty = 12.5 - xc*math.sin(theta) - yc*math.cos(theta)
        # Ty = 240 - blob_image_center[0][1] + 1.25*beta
        # print(Tx, Ty)
        # print(IMG2W(blob_image_center[i][0], blob_image_center[i][1]))

        # for i in range(num_blobs):
        #     xw_yw.append(IMG2W(blob_image_center[i][0], blob_image_center[i][1]))
        xw_yw_zw = IMG2W(blob_image_center[0], blob_image_center[1])
        # print(xw_yw_zw)



    # cv2.namedWindow("Camera View")
    # cv2.imshow("Camera View", image_raw)
    # cv2.namedWindow("Mask View")
    # cv2.imshow("Mask View", mask_image)
    # cv2.namedWindow("Keypoint View")
    # cv2.imshow("Keypoint View", im_with_keypoints)

    # cv2.waitKey(2)

    return xw_yw_zw
