import cv2
import numpy as np
import matplotlib.pyplot as plt
#read the file
capture = cv2.VideoCapture('test.mp4')
#read the nozzle template
nozzle=cv2.imread("nozzle2.jpg",0)        #template for nozzle
h,w=nozzle.shape[:2]                      # rows->h, cols->w

buzzle=0   #debug for nozzle detection's error



while (capture.isOpened()):
    ret, frame = capture.read()
    if ret == 0:
        print("file end!")
        break

    temp = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_LINEAR)
    gray = cv2.cvtColor(temp, cv2.COLOR_BGR2GRAY)

    # Nozzle Detection
    res = cv2.matchTemplate(gray, nozzle, cv2.TM_CCOEFF)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    left_top = max_loc
    right_bottom = (left_top[0] + w, left_top[1] + h + 5)

    # ROI set up
    roiMinX = 0
    roiMaxX = 500
    roiMaxY = 570
    roiMinY = (int)((2 * left_top[1] + h) / 2 + h / 2 - 15)  # 15 reserved sapce

    roi = temp[roiMinY:roiMaxY, roiMinX:roiMaxX]
    if abs(roiMinY - buzzle) > 10 and buzzle != 0:
        print("jump")
        continue
    buzzle = roiMinY
    print("1111")
    # object detection in roi
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    res = np.uint8(np.clip((1.28 * gray + 7.56), 0, 255))  # enhence contrast
    _, thresh = cv2.threshold(res, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    cv2.imshow('thresh', thresh)

    kernel = np.ones((3, 3), np.uint8)
    kernel2 = np.ones((2, 2), np.uint8)
    closing = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)  # 先膨脹在腐蝕(閉合)
    sure_bg = cv2.dilate(closing, kernel2, iterations=3)
    cv2.imshow('roi_surebg', closing)

    dist_transform = cv2.distanceTransform(closing, cv2.DIST_L2, 3)
    ret, sure_fg = cv2.threshold(dist_transform, 0.1 * dist_transform.max(), 255, 0)
    sure_fg = np.uint8(sure_fg)
    cv2.imshow('dist_transform', sure_fg)

    labelnum, labelimg, contours, GoCs = cv2.connectedComponentsWithStats(sure_fg, 4, cv2.CV_32S)
    cv2.rectangle(temp, left_top, right_bottom, (255, 255, 255), 2)  # Mark the detectived nozzle
    for label in range(1, labelnum):
        # x, y = GoCs[label]
        # img = cv2.circle(img2, (int(x), int(y)), 1, (0, 0, 255), -1)
        x_roi, y_roi, w_roi, h_roi, size_roi = contours[label]
        if size_roi > 1000:
            cv2.rectangle(roi, (x_roi, y_roi), (x_roi + w_roi, y_roi + h_roi), (0, 0, 255), 2)

    cv2.imshow('image', temp)
    # cv2.imshow('f', nozzle)
    if cv2.waitKey(30) == ord('q') or cv2.waitKey(30) == ord('Q'):
        cv2.destroyAllWindows()
        break