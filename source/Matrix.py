"""
서보모터 제어 모듈
"""

from __future__ import division
import time
import Adafruit_PCA9685

#BUSNUM = 2
PCA_MODULE_NUM = 8      # PCA9685의 모듈 갯수
PCA_CHANNELS = 16       # 모듈 당 채널 수 (제어 가능한 모터 수)
ROWS = 10               # 행의 수
COLS = 10               # 열의 수

# 행렬 객체 (성분 핸들러)
class Matrix:
    mEntryList = list()
    mPCA9685_Module = list()
    def __init__(self, rows = ROWS, cols = COLS):
        self.mEntryList = list(list() for i in range(rows))
        # 모듈 객체에 Address 할당, Address = 기본 Address | 모듈 번호
        self.mPCA9685_Module = list(Adafruit_PCA9685.PCA9685(hex(0x40|i)) \
            for i in range(PCA_MODULE_NUM))
        for i in range(PCA_MODULE_NUM):
            for j in range(i * PCA_CHANNELS, i * (PCA_CHANNELS + 1) \
                if i * (PCA_CHANNELS + 1) < rows * cols else rows * cols):
                self.mEntryList[j / cols].append(Entry(j / cols, j % cols, self.mPCA9685_Module[i], j % i))
    def __getitem__(self, index):
        return self.mEntryList[index]
    def Initialize(self):
        for el in self.mEntryList:
            for e in el:
                e.applyHeight(0)


# 성분 객체
class Entry:
    row = int(-1)
    col = int(-1)
    module = Adafruit_PCA9685.PCA9685()
    channel = int(-1)
    height = int(0)     # 모터의 높낮이
    speed = int(50)     # 모터의 속도, range 0 ~ 100
    def __init__(self, r, c, m, ch):
        self.row = r             # 성분의 행
        self.col = c             # 성분의 열
        self.module = m          # 모듈 객체
        self.channel = ch        # 모듈에서 할당 된 채널 넘버
    def applyHeight(self, h = -1):
        if h != -1:
            self.height = h
        pulse_length = 1000000    # 1,000,000 us per second
        pulse_length //= 60       # 60 Hz
        # print('{0}us per period'.format(pulse_length))
        pulse_length //= 4096     # 12 bits of resolution
        # print('{0}us per bit'.format(pulse_length))
        h *= 1000
        h //= pulse_length
        return self.module.set_pwm(self.channel, 0, h)  # set_pwm(채널, led_on pwm 신호, led_off pwm 신호)