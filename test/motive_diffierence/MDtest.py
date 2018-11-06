import cv2
import numpy as np
#p136

capture = cv2.VideoCapture('video-1528711687.mp4')
es=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(9,4))    #得到形態學所需的樣板
kernel=np.ones((5,5),np.uint8)
background = None
flag = False
while (capture.isOpened()):
    ret, frame = capture.read()
    if ret == 0:
        print("file end!")
        break
    temp = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_LINEAR)
    # 將第一幀圖像設為背景
    if background is None:
        background = cv2.cvtColor(temp,cv2.COLOR_BGR2GRAY)
        background = cv2.GaussianBlur(background,(9,9),0)
        continue


    #影像前處理
    gray_frame=cv2.cvtColor(temp,cv2.COLOR_BGR2GRAY)
    gray_frame=cv2.GaussianBlur(gray_frame,(9,9),0)


    #difference map
    diff=cv2.absdiff(background,gray_frame)
    diff = cv2.adaptiveThreshold(diff, 255, cv2.ADAPTIVE_THRESH_MEAN_C
                                , cv2.THRESH_BINARY, 11, 4)

    # 將上一張幀當作背景
    background = gray_frame



    cv2.imshow('image', diff)
    #不動的地方會動是因為手機拍攝一定會抖
    #一閃一閃我的猜測是聚焦問題或是光亮

    # cv2.imshow('f', nozzle)
    if cv2.waitKey(30) == ord('q') or cv2.waitKey(30) == ord('Q'):
        break