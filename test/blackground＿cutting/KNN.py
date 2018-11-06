import cv2
import numpy as np
import matplotlib.pyplot as plt

capture = cv2.VideoCapture('file.mp4')
bs = cv2.createBackgroundSubtractorKNN(detectShadows=True)


while (capture.isOpened()):
    ret, frame = capture.read()
    if ret == 0:
        print("file end!")
        break
    temp = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_LINEAR)
    fgmask = bs.apply(temp)
    __,th=cv2.threshold(fgmask.copy(),244,255,cv2.THRESH_BINARY)




    cv2.imshow('image', th)
    #不動的地方會動是因為手機拍攝一定會抖
    #一閃一閃我的猜測是聚焦問題或是光亮


    if cv2.waitKey(30) == ord('q') or cv2.waitKey(30) == ord('Q'):
        break