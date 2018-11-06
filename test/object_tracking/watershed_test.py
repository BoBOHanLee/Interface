#分水嶺演算法嘗試

import cv2
import numpy as np
import matplotlib.pyplot as plt



#影像前處理
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
unknown = cv2.subtract(sure_bg,sure_fg)

#設置柵欄 (連通元件)
ret,markers = cv2.connectedComponents(sure_fg)
markers=markers+1
markers[unknown==255]=0

#打開門讓水進來 並把柵欄會呈紅色
markers=cv2.watershed(img2,markers)
img2[markers==-1] = [0,0,255]

cv2.imshow('test',img2)      #效果不好無法找邊界....................................




#cv2.imshow('test',img)
#cv2.imshow('test',np.hstack((sure_bg,sure_fg)))
k = cv2.waitKey(0)
if k==ord('ｑ'):
    cv2.destroyAllWindows(0)