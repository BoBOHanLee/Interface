import cv2
import numpy as np


img = cv2.imread('test5.jpg',0)
res = cv2.resize(img,None,fx=0.2,fy=0.2,interpolation=cv2.INTER_LINEAR )  #RESIZE photo
equ = cv2.equalizeHist(res)                                               #CONTRAST   (histogram equ)

















cv2.imshow("image",np.hstack([res,equ]))
k = cv2.waitKey(0)
if k==ord('ｑ'):
    cv2.destroyAllWindows(0)