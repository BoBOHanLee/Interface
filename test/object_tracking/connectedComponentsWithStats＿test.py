#嘗試連通元件
import cv2
import numpy as np
import matplotlib.pyplot as plt

##影像前處理
img = cv2.imread('4-OBJECT.jpg')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
res = np.uint8(np.clip((1.28 * gray + 7.56), 0, 255))  #對比
ret,thresh = cv2.threshold(res,100,255,cv2.THRESH_BINARY_INV)

img2 = cv2.resize(img,None,fx=2,fy=2,interpolation=cv2.INTER_LINEAR)
res2 = cv2.resize(res,None,fx=2,fy=2,interpolation=cv2.INTER_LINEAR)
thresh2 = cv2.resize(thresh,None,fx=2,fy=2,interpolation=cv2.INTER_LINEAR)

#形態學
kernel = np.ones((4,4),np.uint8)
kernel2 = np.ones((3,3),np.uint8)
closing = cv2.morphologyEx(thresh2,cv2.MORPH_CLOSE,kernel,iterations=2) #先膨脹在腐蝕
sure_bg = cv2.dilate(closing,kernel2,iterations=3)

#獲取確定的前景區域
dist_transform=cv2.distanceTransform(closing,cv2.DIST_L2,3)
ret,sure_fg = cv2.threshold(dist_transform,0.05*dist_transform.max(),255,0)
sure_fg = np.uint8(sure_fg)
#cv2.imshow('test2',np.hstack((sure_bg,sure_fg)))

labelnum, labelimg, contours, GoCs = cv2.connectedComponentsWithStats(sure_fg ,4, cv2.CV_32S)

for label in range(1, labelnum):
    #x, y = GoCs[label]
    #img = cv2.circle(img2, (int(x), int(y)), 1, (0, 0, 255), -1)
    x, y, w, h, size = contours[label]
    if size>30:
      img = cv2.rectangle(img2, (x, y), (x + w, y + h), (0, 0, 255), 1)

cv2.imshow('test',img)   # 可行 但要如何納參數統一又是另一到問題了

k = cv2.waitKey(0)
if k==ord('ｑ'):
    cv2.destroyAllWindows(0)