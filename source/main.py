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

class mainWindow(QMainWindow, main_form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # 전체화면 설정
        self.showFullScreen()
        self.BluetoothButton.clicked.connect(self.BluetoothClicked)
        self.KinectButton.clicked.connect(self.KinectClicked)
        self.SnakeButton.clicked.connect(self.SnakeClicked)
        #self.m = Matrix(ROWS, COLS)
        #self.m.syncActivate()
        #self.m.setHeight(SERVO_MIN)
    def BluetoothClicked(self):
        dlg = audioDialog()
        dlg.exec_()
    def KinectClicked(self):
        #self.k.threadActvate(True)  # 키넥트 스레드 시작
        dlg = kinectDialog()
        dlg.exec_()
    def SnakeClicked(self):
        dlg = snakeDialog()
        dlg.exec_()

class kinectDialog(QDialog, kinect_form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # 전체화면 설정
        self.showFullScreen()
        self.backButton.clicked.connect(self.backClicked)
        self.k = Kinect()
        self.k.threadActivate()
    def backClicked(self):
        self.close()

class audioDialog(QDialog, audio_form_class):
    a = AudioSpectrum()
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # 전체화면 설정
        self.showFullScreen()
        self.a.threadActivate(True)     # 오디오 스레드 활성화
        self.backButton.clicked.connect(self.backClicked)
        self.disconnectButton.clicked.connect(self.disconnectClicked)
    def backClicked(self):
        self.a.threadActivate(False)    # 오디오 스레드 비활성화
        self.close()
    def disconnectClicked(self):
        os.system("bluetoothctl disconnect")

class snakeDialog(QDialog, snake_form_class):
    s = Snake()
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # 전체화면 설정
        self.showFullScreen()
        self.backButton.clicked.connect(self.backClicked)
    def backClicked(self):
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = mainWindow()
    myWindow.show()
    app.exec_()

def mainThread(k,m):
    while(True):
        k.getDepth()
        #print(a.plot3D)
        m.setKinectHeight(k.depth)
        time.sleep(0.0001)
