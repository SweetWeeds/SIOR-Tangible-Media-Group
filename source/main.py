from Matrix import *
from Kinect import *
from Audio import *
from Snake import *
import threading
import time
import sys
import os
from PyQt5.QtWidgets import *
from PyQt5 import uic, QtGui
import PyQt5

main_form_class = uic.loadUiType("UI/main.ui")[0]
kinect_form_class = uic.loadUiType("UI/camera.ui")[0]
audio_form_class = uic.loadUiType("UI/audio.ui")[0]
snake_form_class = uic.loadUiType("UI/snake.ui")[0]

ROWS = 9
COLS = 9
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
        self.mMode = 0
        self.moduleThread = threading.Thread(target=self.moduleSyncThread)
        self.moduleThread.start()
        #self.k.threadActivate()
        self.s = Snake()
    def KinectClicked(self):
        self.mMode = 1
        self.k.threadActivate(True)  # 키넥트 스레드 시작
        dlg = kinectDialog()
        dlg.exec_()
        if dlg.isBackClicked == True:
            print("종료")
            self.mMode = 0
            self.k.threadActivate(False)
    def BluetoothClicked(self):
        self.mMode = 2
        self.a.threadActivate(True)
        dlg = audioDialog()
        dlg.exec_()
        if dlg.isBackClicked == True:
            self.mMode = 0
            self.a.threadActivate(False)
    def SnakeClicked(self):
        self.mMode = 3
        dlg = snakeDialog(self)
        dlg.exec_()
        if dlg.isBackClicked == True:
            self.mMode = 0
    def moduleSyncThread(self):
        while(True):
            # 1. 키넥트
            if(self.mMode == 1):
                #self.k.getDepth()
                print(self.k.depth)
                #print('키넥트')
                self.m.setKinectHeight(self.k.depth)
                time.sleep(0.0001)
            # 2. 오디오
            elif(self.mMode == 2):
                self.m.setKinectHeight(self.a.depth)
                time.sleep(0.0001)
            # 3. 스네이크
            elif(self.mMode == 3):
                #print("스네잌   ")
                self.m.setKinectHeight(self.s.map + SERVO_MIN)
                #print(self.s.map)
                #self.m.setKinectHeight(self.s.map)
                time.sleep(0.0001)
            time.sleep(0.0001)
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
        self.backButton.clicked.connect(self.backClicked)
        self.disconnectButton.clicked.connect(self.disconnectClicked)
    def backClicked(self):
        self.isBackClicked = True
        self.close()
    def disconnectClicked(self):
        os.system("bluetoothctl disconnect")

class snakeDialog(QDialog, snake_form_class):
    isBackClicked = False
    def __init__(self, motherClass):
        super().__init__()
        self.setupUi(self)
        # 전체화면 설정
        #self.showFullScreen()
        self.backButton.clicked.connect(self.backClicked)
        self.startButton.clicked.connect(self.startClicked)
        self.leftButton.clicked.connect(self.leftClicked)
        self.rightButton.clicked.connect(self.rightClicked)
        self.upButton.clicked.connect(self.upClicked)
        self.downButton.clicked.connect(self.downClicked)
        self.timer = PyQt5.QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.motherClass = motherClass
        #self.s = self.motherClass.s
    def update(self):
        if self.motherClass.s.worm.check_ahead_gold(self.motherClass.s.gold):
            self.motherClass.s.worm.move_to_direction(True)
            self.motherClass.s.gold.set_position(self.motherClass.s.get_empty_position())
        else:
            self.motherClass.s.worm.move_to_direction(False)

        if self.motherClass.s.worm.check_collision():
            self.timer.stop()
        else:
            self.motherClass.s.draw_matrix()
            self.timer.start(1000)
    def backClicked(self):
        print("뒤로")
        self.isBackClicked = True
        self.close()
    def startClicked(self):
        self.motherClass.s = Snake()
        self.timer.start(0)
    def leftClicked(self):
        self.motherClass.s.worm.set_left()
    def rightClicked(self):
        self.motherClass.s.worm.set_right()
    def upClicked(self):
        self.motherClass.s.worm.set_up()
    def downClicked(self):
        self.motherClass.s.worm.set_down()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = mainWindow()
    myWindow.show()
    app.exec_()

