"""
서보모터 제어 모듈
"""

from __future__ import division
import time
import Adafruit_PCA9685
import threading
import numpy as np

#BUSNUM = 2
PCA_MODULE_NUM = 2      # PCA9685의 모듈 갯수
PCA_CHANNELS = 16       # 모듈 당 채널 수 (제어 가능한 모터 수)
ROWS = 8                # 행의 수
COLS = 8                # 열의 수
SERVO_MIN = 130         # Min pulse length out of 4096
SERVO_MAX = 630         # Max pulse length out of 4096

# 행렬 객체 (성분 핸들러)
class Matrix:
    mEntryList = list()
    mPCA9685_Module = list()
    def __init__(self, rows = ROWS, cols = COLS):
        self.mEntryList = list(list() for i in range(rows))
        # 모듈 객체에 Address 할당, Address = 기본 Address | 모듈 번호
        for i in range(int((rows * cols) / PCA_CHANNELS)):
            try:
                self.mPCA9685_Module.append(Adafruit_PCA9685.PCA9685(address=0x40|i))
                self.mPCA9685_Module[-1].set_pwm_freq(50)   # set freq to 60hz
            except:
                print("ERROR:{}번째 모듈을 할당 할 수 없습니다.".format(0x40|i))
            for j in range(i * PCA_CHANNELS, (i + 1) * PCA_CHANNELS):
                try:
                    print("i:{},f:{}".format(i,j))
                    print("Channel :{}".format(j % PCA_CHANNELS))
                    self.mEntryList[int(j / cols)].append(Entry(int(j / cols), j % cols, self.mPCA9685_Module[i], j % PCA_CHANNELS))
                except:
                    print("ERROR: mEntryList의 {}번째 리스트를 인덱싱 할 수 없습니다.".format(int(j/cols)))
    def __getitem__(self, index):
        return self.mEntryList[index]
    """
    def setAllHeight(self, h = SERVO_MAX):
        for el in self.mEntryList: 
            for e in el:
                print('[{}][{}] module:{} channel:{}'.format(e.row, e.col, e.module, e.channel))
                e.height = h
    """
    def setHeight(self, arg1):
        # if arg1's type is ndarray
        if(type(arg1) == type(np.ndarray(1))):
            for i in len(self.mEntryList):
                for j in len(self.mEntryList[0]):
                    self.mEntryList[i][j].applyHeight(arg1[i][j])
        # if arg1's type is integer
        elif(type(arg1) == type(int())):
            for el in self.mEntryList: 
                for e in el:
                    e.height = arg1
    def syncActivate(self, Act = True):
        for el in self.mEntryList:
            for e in el:
                e.syncActivate(Act)


# 성분 객체
class Entry:
    row = int(-1)
    col = int(-1)
    module = Adafruit_PCA9685.PCA9685()
    channel = int(-1)
    height = int(0)     # 모터의 높낮이
    speed = int(50)     # 모터의 속도, range 0 ~ 100
    syncActive = False  # 싱크 작동 여부
    syncThread = None
    def __init__(self, r, c, m, ch):
        self.row = r             # 성분의 행
        self.col = c             # 성분의 열
        self.module = m          # 모듈 객체
        self.channel = ch        # 모듈에서 할당 된 채널 넘버
        self.applyHeight(SERVO_MIN)
    def syncHeight(self):
        print("[{}][{}] Motor Sync Thread Start (Module Name {}, Channel {})".format(self.row, self.col, self.module, self.channel))
        while(self.syncActive):
            try:
                self.module.set_pwm(self.channel, 0, self.height)
                #print('[{}][{}] module:{} channel:{}'.format(self.row, self.col, self.module, self.channel))
            except:
                print("[ERROR] syncHeight, channel:{}, height:{}".format(self.channel, self.height))
            time.sleep(0.05)
    def syncActivate(self, Act = True):
        if(Act and self.syncThread == None):
            self.syncActive = True
            self.syncThread = threading.Thread(target=self.syncHeight)
            self.syncThread.start()
        elif(Act and self.syncThread != None):
            print('[ERROR] thread is already exist.')
            return
        else:
            self.syncActive = False
            self.syncThread = None
    def applyHeight(self, h = -1):
        if h != -1:
            self.height = h

if __name__ == "__main__":
    print("매트릭스 모듈 테스트 시작")
    m = Matrix(8,4)
    m.syncActivate()
    m.setHeight(SERVO_MIN)
    while(True):
        for i in range(SERVO_MIN,SERVO_MAX,10):
            print(i)
            m.setHeight(i)
            time.sleep(0.05)
        for i in range(SERVO_MAX,SERVO_MIN,-10):
            print(i)
            m.setHeight(i)
            time.sleep(0.05)
