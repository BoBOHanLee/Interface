import cv2
import numpy as np



def hisEqulColor(img):          #CONTRAST colorful  (histogram equ)
    ycrcb = cv2.cvtColor(img, cv2.COLOR_BGR2YCR_CB)
    channels = cv2.split(ycrcb)
    cv2.equalizeHist(channels[0], channels[0])
    cv2.merge(channels, ycrcb)
    cv2.cvtColor(ycrcb, cv2.COLOR_YCR_CB2BGR, img)
    return img

def sharpen(img):     #銳化雜訊太多  不適用
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    kernel2=np.array([[-1,-1,-1],[-1,7,-1],[-1,-1,-1]])
    dst = cv2.filter2D(img, -1, kernel=kernel)
    return dst


def template(img,temp):
    h, w = temp.shape[:2]  ## rows->h, cols->w
    res = cv2.matchTemplate(img, temp, cv2.TM_CCOEFF)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)
    cv2.rectangle(img, top_left, bottom_right, (255, 255, 255), 2)
    return img


# preprocess
img = cv2.imread('../test_photo/test4.jpg')
res = cv2.resize(img,None,fx=0.2,fy=0.2,interpolation=cv2.INTER_LINEAR )  #RESIZE photo

res_show=res.copy()
equ = hisEqulColor(res)



#template
equ_show=equ.copy()
temp=cv2.imread('nozzle.jpg')
nozzle_tra=template(equ,temp)







cv2.imshow("image",np.hstack([res_show,equ_show,nozzle_tra]))
k = cv2.waitKey(0)
if k==ord('ｑ'):
    cv2.destroyAllWindows(0)