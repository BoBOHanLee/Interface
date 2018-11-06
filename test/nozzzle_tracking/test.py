import cv2
import numpy as np
import matplotlib.pyplot as plt

#模板匹配就是用来在大图中找小图，也就是说在一副图像中寻找另外一张模板图像的位置
#模板匹配的原理其实很简单，就是不断地在原图中移动模板图像去比较，有6种不同的比较方法

capture = cv2.VideoCapture('video.mp4')
nozzle=cv2.imread("nozzle2.jpg",0)
#temp_nz = cv2.resize(nozzle, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_LINEAR)
h,w=nozzle.shape[:2] ## rows->h, cols->w


while (capture.isOpened()):
    ret, frame = capture.read()   # 函数返回的第1个参数ret(return value缩写)是一个布尔值，表示当前这一帧是否获取正确
    temp = cv2.resize(frame, None, fx=0.8, fy=0.8, interpolation=cv2.INTER_LINEAR)
    gray = cv2.cvtColor(temp, cv2.COLOR_BGR2GRAY)  # 将这帧转换为灰度图
    res = cv2.matchTemplate(gray, nozzle, cv2.TM_CCOEFF)  # 匹配函数返回的是一副灰度图，最白的地方表示最大的匹配
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)  # 得到最大匹配值的坐标，以这个点为左上角角点，模板的宽和高画矩形就是匹配的位置了
    left_top = max_loc  # 左上角
    right_bottom = (left_top[0] + w, left_top[1] +h+5)  # 右下角
    cv2.rectangle(temp, left_top, right_bottom,(255,255,255), 2)  # 画出矩形位置
    cv2.imshow('frame', temp)
   # cv2.imshow('f', nozzle)
    if cv2.waitKey(30) == ord('q'): #注意Q無法中斷喔! 須小寫
        break






