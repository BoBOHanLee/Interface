import cv2
import numpy as np
import matplotlib.pyplot as plt

capture = cv2.VideoCapture('file.mp4')
mog = cv2.createBackgroundSubtractorMOG2()

while (capture.isOpened()):
    ret, frame = capture.read()
    if ret == 0:
        print("file end!")
        break
    temp = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_LINEAR)
    fgmask = mog.apply(temp)



    cv2.imshow('image', fgmask)
    #不動的地方會動是因為手機拍攝一定會抖
    #一閃一閃我的猜測是聚焦問題或是光亮


    if cv2.waitKey(30) == ord('q') or cv2.waitKey(30) == ord('Q'):
        break