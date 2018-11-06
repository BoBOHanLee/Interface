# to mark out the position of nozzle and output ROI
from __future__ import print_function
import cv2
import numpy as np

MAX_FEATURES = 500
GOOD_MATCH_PERCENT = 0.1  #取匹配效果最好的前10%

# nozzle tracking for feature match
def alignImages(im1, im2):                  #噴頭的特徵比對  但目前照面模糊  無法跑出特徵匹配的效果
    # Convert images to grayscale


    im1Gray = cv2.cvtColor(im1, cv2.COLOR_BGR2GRAY)
    im2Gray = cv2.cvtColor(im2, cv2.COLOR_BGR2GRAY)


    # Detect ORB features and compute descriptors.
    orb = cv2.ORB_create(MAX_FEATURES)
    keypoints1, descriptors1 = orb.detectAndCompute(im1Gray, None)
    keypoints2, descriptors2 = orb.detectAndCompute(im2Gray, None)



    # Match features.
    matcher = cv2.DescriptorMatcher_create(cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING)    # use the way of Brute-Force
    matches = matcher.match(descriptors1, descriptors2, None)

    # Sort matches by score
    matches.sort(key=lambda x: x.distance, reverse=False)  #將匹配分數由最好排到最低

    # Remove not so good matches
    numGoodMatches = int(len(matches) * GOOD_MATCH_PERCENT)
    matches = matches[:numGoodMatches]


    # Draw top matches
    imMatches = cv2.drawMatches(im1, keypoints1, im2, keypoints2, matches, None)
    #cv2.imwrite("matches.jpg", imMatches)

    # Extract location of good matches
    points1 = np.zeros((len(matches), 2), dtype=np.float32)      # ( x,y )
    points2 = np.zeros((len(matches), 2), dtype=np.float32)

    for i, match in enumerate(matches):                          # enumerate 索引以及索引對應到的值
        points1[i, :] = keypoints1[match.queryIdx].pt
        points2[i, :] = keypoints2[match.trainIdx].pt


    # Find homography   轉換矩陣 以匹配點來計算
    h, mask = cv2.findHomography(points1, points2, cv2.RANSAC)

    # Use homography
    height, width, channels = im2.shape
    im1Reg = cv2.warpPerspective(im1, h, (width, height))




    # cal. the most lower nozzle point
    cup=0
    num_xy=0
    for i , XY in enumerate(points2):
        if XY[1] > cup:
            cup = XY[1]
            num_xy=i
        else:
            continue

    cv2.circle(im2, (points2[num_xy,0],points2[num_xy,1]) ,10, (0, 0, 255), -1)
    #im2 = cv2.resize(im2, None, fx=0.3, fy=0.3, interpolation=cv2.INTER_LINEAR)
    #cv2.imshow('nozzle',im2)
    cv2.imwrite('nozzle.jpg',im2)

    

    return im1Reg, h

