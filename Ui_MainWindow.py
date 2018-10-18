import sys
import cv2
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QDockWidget, QListWidget
from PyQt5.QtGui import *
import threading
import time

from UI_design.test import Ui_MainWindow
from UI_design.close_dialog import Ui_Dialog as Ui_Dialog_close
import ROI_process




class mywindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self):
        super(mywindow, self).__init__()
        self.setupUi(self)
        self.show_bottom.clicked.connect(self.threading_showImage)   #以多線程 跑shownig image
        self.close_botton.clicked.connect(self.click_closeButton)




    #顯示關閉視窗的對話窗口
    def click_closeButton(self):

        Dialog = QtWidgets.QDialog()
        ui =Ui_Dialog_close()
        ui.setupUi(Dialog)
        Dialog.show()
        #Dialog.exec_()

        rsp = Dialog.exec_()
        if rsp == QtWidgets.QDialog.Accepted:   #，QtWidgets.QDialog.Accepted  對話框的接收事件
            self.close()
        else:
            self.show()


    #背景一直顯示圖片和roi
    def showImage_fuction(self):      # for showing image
        while True:                   #以多進程方式每隔一秒就讀取顯示
            time.sleep(1)
            # -----------------------Image Processing-----------------------------#

            # nozzle tracking
            im = cv2.imread("test_photo/head.jpg", cv2.IMREAD_COLOR)
            imReference = cv2.imread("test_photo/3.jpg", cv2.IMREAD_COLOR)  # 1.jpg就是之後樹梅派要一直傳進來的圖片
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
          thread = threading.Thread(target=self.showImage_fuction)  # 定义线程
          thread.start()  # 让线程开始工作







if __name__ == '__main__':



    app = QtWidgets.QApplication(sys.argv)
    window = mywindow()
    window.show()
    sys.exit(app.exec_())