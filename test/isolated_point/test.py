import cv2
import numpy as np
import matplotlib.pyplot as plt


img=cv2.imread('fail.jpg',0)
#img=cv2.imread('elephant.jpg',0)
#img=cv2.imread('deep.jpg',0)
_, th = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
kernel = np.array([[1,1,1],[1,-8,1],[1,1,1]])
dst = cv2.filter2D(th, -1, kernel)   #中間的數為-1，輸出數值格式的相同
#laplacian = cv2.Laplacian(th, -1)   #效果同上

#垂直投影變化
(h,w)=dst.shape #返回高和宽
print(h,w)
count_v=[0 for x in range(0,w)]      #紀錄垂直變化的總數(對每一行)
for j in range(0,w): #每一行
    for i in range(1,h):  #每一列
        temp=int(dst[i,j])-int(dst[i-1,j])    #強制為整數相減財部會溢出
        if 255 == abs(temp):  #如果每一行相鄰兩像素為黑白則黑白次數加一
            count_v[j] = count_v[j]+1
print(count_v)


#水平投影變化
count_h=[0 for x in range(0,h)]
for i in range(0,h):  #每一列
    for j in range(1,w): #每一行
        temp=int(dst[i,j])-int(dst[i,j-1])    #強制為整數相減財部會溢出
        if 255 == abs(temp):  #如果每一行相鄰兩像素為黑白則黑白次數加一
            count_h[i] = count_v[i]+1
print(count_h)

#show
cv2.imshow("gray",img)
cv2.imshow("before",th)
cv2.imshow("after filter",dst)
k = cv2.waitKey(0)
if k==ord('ｑ'):
    cv2.destroyAllWindows(0)