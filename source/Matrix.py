"""
서보모터 제어 모듈
"""

from __future__ import division
import time
import Adafruit_PCA9685
import threading
import numpy as np

#BUSNUM = 2
PCA_CHANNELS = 16       # 모듈 당 채널 수 (제어 가능한 모터 수)
ROWS = 9                # 행의 수
COLS = 9                # 열의 수
SERVO_MIN = 100         # 가장 높은 높이
SERVO_MAX = 450         # 가장 낮은 높이
ADDR_START = 0x40

# 행렬 객체 (성분 핸들러)
class Matrix:
    mEntryList = list()
    mPCA9685_Module = list()
    def __init__(self, rows = ROWS, cols = COLS):
        self.mEntryList = list(list() for i in range(rows))
        # 모듈 객체에 Address 할당, Address = 기본 Address | 모듈 번호
        module_num = int((rows * cols) / PCA_CHANNELS) + 1
        #print(module_num)
        for i in range(module_num):
            #print(i)
            try:
                self.mPCA9685_Module.append(Adafruit_PCA9685.PCA9685(address=ADDR_START|i))
                self.mPCA9685_Module[-1].set_pwm_freq(50)   # set freq to 60hz
            except:
                #print("ERROR:{}번째 모듈을 할당 할 수 없습니다.".format(ADDR_START|i))
                pass
            for j in range(i * PCA_CHANNELS, (i + 1) * PCA_CHANNELS if (((i + 1) * PCA_CHANNELS) < ROWS * COLS) else ROWS * COLS):
                try:
                    print("Address:{}, i:{},f:{}".format(hex(ADDR_START|i), i,j))
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
    def setKinectHeight(self, arg1):
        #print(arg1)
        #print("height")
        minHeight = np.min(arg1)
        maxHeight = np.max(arg1)

        #arg1 = (arg1 * (SERVO_MAX - SERVO_MIN) / (maxHeight - minHeight if (maxHeight - minHeight != 0) else 1) + SERVO_MIN)
        arg1 = (arg1 * (SERVO_MAX - SERVO_MIN) / 255 + SERVO_MIN)
        self.setHeight(arg1)
        print(arg1)
    def setHeight(self, arg1):
        # if arg1's type is ndarray
        if(type(arg1) == type(np.ndarray(1))):
            for i in range(len(self.mEntryList)):
                for j in range(len(self.mEntryList[0])):
                    try:
                        self.mEntryList[i][j].applyHeight(arg1[i][j])
                    except:
                        #print("[ERROR] {},{}번째 모듈을 제어할 수 없습니다.".format(i,j))
                        pass
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
    threadActive = True  # 싱크 작동 여부
    def __init__(self, r, c, m, ch):
        self.row = r             # 성분의 행
        self.col = c             # 성분의 열
        self.module = m          # 모듈 객체
        self.channel = ch        # 모듈에서 할당 된 채널 넘버
        self.applyHeight(SERVO_MIN)
        self.syncThread = threading.Thread(target=self.syncHeight)
        self.syncThread.start()
    def syncHeight(self):
        print("[{}][{}] Motor Sync Thread Start (Module Name {}, Channel {})".format(self.row, self.col, self.module, self.channel))
        while(True):
            self.module.set_pwm(self.channel, 0, self.height)
            time.sleep(0.05)
    def syncActivate(self, Act = True):
        if Act == True:
            return
        elif self.threadActive == False and Act == True:
            print("키넥트 스레드 활성화")
            self.threadActive = True
        else:
            self.threadActive = False
    def applyHeight(self, h = -1):
        if h != -1 and h != np.nan:
            self.height = int(h)

if __name__ == "__main__":
    print("매트릭스 모듈 테스트 시작")
    m = Matrix(9,9)
    m.syncActivate()
    m.setHeight(SERVO_MIN)
    while(True):
        print('1: 최소~최대 테스트')
        print('2: 값 수동 입력')
        cmd = input('테스트 종류 선택: ')
        if(cmd == '1'):
            for i in range(SERVO_MIN,SERVO_MAX,5):
                print(i)
                m.setHeight(i)
                time.sleep(0.005)
            for i in range(SERVO_MAX,SERVO_MIN,-5):
                print(i)
                m.setHeight(i)
                time.sleep(0.005)
        elif(cmd == '2'):
            val = SERVO_MIN
            while(val != -1):
                val = input('값 입력: ')
                m.setHeight(int(val))
