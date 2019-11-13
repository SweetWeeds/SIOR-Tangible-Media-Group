#from Matrix import *
from Kinect import *
from Audio import *
import threading
import time
import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic

form_class = uic.loadUiType("UI/main.ui")[0]

ROWS = 3
COLS = 10

class MyWindow(QMainWindow, form_class):
    a = AudioSpectrum()
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # 전체화면 설정
        #self.showFullScreen()
        self.BluetoothButton.clicked.connect(self.)
    def BluetoothSpeaker(self):
        self.a.threadActvate(True)  # 오디오 스레드 시작
    def Kinect(self):
        self.k.threadActvate(True)  # 키넥트 스레드 시작
    def Snake(self):
        self.

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()

def mainThread(k,m):
    while(True):
        k.getDepth()
        #print(a.plot3D)
        m.setKinectHeight(k.depth)
        time.sleep(0.0001)
