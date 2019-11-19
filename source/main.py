#from Matrix import *
from Kinect import *
from Audio import *
from Snake import *
import threading
import time
import sys
import os
from PyQt5.QtWidgets import *
from PyQt5 import uic

main_form_class = uic.loadUiType("UI/main.ui")[0]
kinect_form_class = uic.loadUiType("UI/camera.ui")[0]
audio_form_class = uic.loadUiType("UI/audio.ui")[0]
snake_form_class = uic.loadUiType("UI/snake.ui")[0]

ROWS = 3
COLS = 10
def mainThread(k,m):
    while(True):
        k.getDepth()
        #print(a.plot3D)
        m.setKinectHeight(k.depth)
        time.sleep(0.0001)

class mainWindow(QMainWindow, main_form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # 전체화면 설정
        self.showFullScreen()
        self.BluetoothButton.clicked.connect(self.BluetoothClicked)
        self.KinectButton.clicked.connect(self.KinectClicked)
        self.SnakeButton.clicked.connect(self.SnakeClicked)
        self.m = Matrix(ROWS, COLS)
        self.m.syncActivate()
        self.m.setHeight(SERVO_MIN)
        self.a = AudioSpectrum()
        self.k = Kinect()
        self.k.threadActivate()
        self.s = Snake()
        self.mode = 0
    def KinectClicked(self):
        self.mode = 1
        self.k.threadActivate(True)  # 키넥트 스레드 시작
        dlg = kinectDialog()
        dlg.exec_()
        if dlg.isBackClicked == True:
            self.mode = 0
            self.k.threadActivate(False)
    def BluetoothClicked(self):
        self.mode = 2
        self.a.threadActivate(True)
        dlg = audioDialog()
        dlg.exec_()
        if dlg.isBackClicked == True:
            self.mode = 0
            self.a.threadActivate(False)
    def SnakeClicked(self):
        self.mode = 3
        dlg = snakeDialog()
        dlg.exec_()
    def moduleSyncThread(self):
        while(True):
            # 1. 키넥트
            if(self.mode == 1):
                #self.k.getDepth()
                #print(a.plot3D)
                self.m.setKinectHeight(k.depth)
                time.sleep(0.0001)
            # 2. 오디오
            elif(self.mode == 2):
                self.m.setHeight(self.a.depth)
                time.sleep(0.0001)
            # 3. 스네이크
            elif(self.mode == 3)
            else:
                sleep(1)
                continue
class kinectDialog(QDialog, kinect_form_class):
    isBackClicked = False
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # 전체화면 설정
        self.showFullScreen()
        self.backButton.clicked.connect(self.backClicked)
    def backClicked(self):
        self.isBackClicked = True
        self.close()

class audioDialog(QDialog, audio_form_class):
    isBackClicked = False
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # 전체화면 설정
        self.showFullScreen()
        self.a.threadActivate(True)     # 오디오 스레드 활성화
        self.backButton.clicked.connect(self.backClicked)
        self.disconnectButton.clicked.connect(self.disconnectClicked)
    def backClicked(self):
        self.isBackClicked = True
        self.a.threadActivate(False)    # 오디오 스레드 비활성화
        self.close()
    def disconnectClicked(self):
        os.system("bluetoothctl disconnect")

class snakeDialog(QDialog, snake_form_class):
    isBackClicked = False
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # 전체화면 설정
        self.showFullScreen()
        self.backButton.clicked.connect(self.backClicked)
    def backClicked(self):
        self.isBackClicked = True
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = mainWindow()
    myWindow.show()
    app.exec_()

