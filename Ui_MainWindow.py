import sys
import cv2
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QDockWidget, QListWidget
from PyQt5.QtGui import *
import threading
import time
import socket

from UI_design.gcode_trasn import Ui_Form as Ui_Form_gcodeTrans
from UI_design.test import Ui_MainWindow
from UI_design.close_dialog import Ui_Dialog as Ui_Dialog_close
import ROI_process



#gcode視窗
class gcodeWindow(QtWidgets.QWidget,Ui_Form_gcodeTrans):

     def __init__(self):
         super(gcodeWindow, self).__init__()
         self.setupUi(self)

     def handle_click(self):
         if not self.isVisible():
             self.show()

     def handle_close(self):
         self.close()


#主視窗
class mywindow(QtWidgets.QMainWindow, Ui_MainWindow):


    def __init__(self):
        super(mywindow, self).__init__()
        self.setupUi(self)


        # 點擊影像串流後以多線程方式無限迴圈刷新圖片以及顯示
        self.thread_showImage = threading.Thread(target=self.showImage_fuction)  # 定义线程
        self.show_bottom.clicked.connect(self.threading_showImage)   #以多線程 跑shownig image

        # 點擊關閉後跳出關閉視窗
        self.close_botton.clicked.connect(self.click_closeButton)

        #點擊開啟gcode傳輸視窗
        #self.gcode_button.clicked.connect(self.click_showGcodeWin)





    def click_closeButton(self):


        Dialog = QtWidgets.QDialog()
        ui = Ui_Dialog_close()
        ui.setupUi(Dialog)
        Dialog.show()
        # Dialog.exec_()

        # 關閉連線
        conn.close()
        socket_1.close()
        print('server close')

        rsp = Dialog.exec_()
        if rsp == QtWidgets.QDialog.Accepted:  # ，QtWidgets.QDialog.Accepted  對話框的接收事件
            self.close()
            self.threading_showImage.exit()    #關閉影像串流線程
        else:
            self.show()



    def showImage_fuction(self):      # for showing image


        while True:                   #以多進程方式每隔一秒就讀取顯示
            time.sleep(1)

            #----------------------Image Accept-----------------------------------#
            print('begin write image file "0001.jpg"')
            imgFile = open('test_photo/0001.jpg', 'wb')
            while True:
                imgData = conn.recv(512)  # 接收遠端主機傳來的數據
                if not imgData:
                    break  # 讀完檔案結束迴圈
                imgFile.write(imgData)
            imgFile.close()
            print('image save')

            # -----------------------Image Processing-----------------------------#

            # nozzle tracking
            im = cv2.imread("test_photo/head.jpg", cv2.IMREAD_COLOR)
            imReference = cv2.imread("test_photo/0001.jpg", cv2.IMREAD_COLOR)  # 就是之後樹梅派要一直傳進來的圖片
            __, h = ROI_process.alignImages(im, imReference)
            print("Estimated homography : \n", h)

            # main
            img = cv2.imread('nozzle.jpg')
            img = cv2.resize(img, (261, 441))
            image_height, image_width, image_depth = img.shape

            # roi
            img_roi = cv2.imread('roi.jpg')
            img_roi = cv2.resize(img_roi, (111, 61))
            roi_height, roi_width, roi_depth = img_roi.shape

            # -------------- Qimge to show on the interface-----------------------#
            # main
            QImg = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            QImg = QImage(QImg.data, image_width, image_height,
                          image_width * image_depth,
                          QImage.Format_RGB888)
            self.img_main.setPixmap(QPixmap.fromImage(QImg))

            # roi
            QImg_roi = cv2.cvtColor(img_roi, cv2.COLOR_BGR2RGB)
            QImg_roi = QImage(QImg_roi.data, roi_width, roi_height,
                              roi_width * roi_depth,
                              QImage.Format_RGB888)
            self.img_roi.setPixmap(QPixmap.fromImage(QImg_roi))
            # ---------------------------------------------------------------------#

    def threading_showImage(self):
         # thread = threading.Thread(target=self.showImage_fuction)  # 定义线程
          self.thread_showImage.start()  # 让线程开始工作







# show gcode transport window




if __name__ == '__main__':
    # ----------------------建立連線------------------- #
    host = '192.168.0.108'  # 對server端為主機位置
    port = 7654
    address = (host, port)
    socket_1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  ## AF_INET:默認IPv4, SOCK_STREAM:TCP

    socket_1.bind(address)
    socket_1.listen(1)  # 系統可以掛起的最大連接數量。該值至少為1
    print('socket startup')

    conn, addr = socket_1.accept()  # 接受遠程計算機的連接請求，建立起與客戶機之間的通信連接
    # conn是新的套接字對象，可以用來接收和發送數據。address是連接客戶端的地址
    print('Connected by', addr)



    #--------------------------- G U I ---------------------#
    app = QtWidgets.QApplication(sys.argv)
    window = mywindow()

    #顯示gocde視窗
    gwindow = gcodeWindow()
    window.gcode_button.clicked.connect(gwindow.handle_click)



    window.show()
    sys.exit(app.exec_())