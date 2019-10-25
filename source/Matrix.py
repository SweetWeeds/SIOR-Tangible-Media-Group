"""
서보모터 제어 모듈
"""

from __future__ import division
import time
import Adafruit_PCA9685

PCA_MODULE_NUM = 8      # PCA9685의 모듈 갯수
PCA_CHANNELS = 16       # 모듈 당 채널 수 (제어 가능한 모터 수)
ROWS = 10               # 행의 수
COLS = 10               # 열의 수

# 행렬 객체 (성분 핸들러)
class Matrix:
    def __init__(self, rows, cols):
        """ 성분 2차원 리스트 초기화 """
        mEntryList = list(None for i in range(rows))
        # 모듈 객체에 Address 할당, Address = 기본 Address | 모듈 번호
        mPCA9685_Module = list(Adafruit_PCA9685.PCA9685(hex(0x40|i)) \
            for i in range(PCA_MODULE_NUM))
        for i in range(PCA_MODULE_NUM):
            for j in range(i * PCA_CHANNELS, i * (PCA_CHANNELS + 1) \
                if i * (PCA_CHANNELS + 1) < rows * cols else rows * cols):
                mEntryList[j / cols].append(Entry(j / cols, j % cols, mPCA9685_Module[i], j % i))

# 성분 객체
class Entry:
    def __init__(self, r, c, m, ch):
        row = r             # 성분의 행
        col = c             # 성분의 열
        module = m          # 모듈 객체
        channel = ch        # 모듈에서 할당 된 채널 넘버
        height = int(0)     # 모터의 높낮이
        speed = int(50)     # 모터의 속도, range 0 ~ 100
    def applyHeight(self):
        m.set_pwm(ch, 0, )  # set_pwm(채널, led_on pwm 신호, led_off pwm 신호)