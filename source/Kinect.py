import numpy as np
import sys
import threading
from freenect import sync_get_depth as get_depth
import time
import queue
from functools import reduce

disp_size = (640, 480)
ROWS = 9
COLS = 9

ROW_DIV = disp_size[0] / ROWS
COL_DIV = disp_size[1] / COLS

class Kinect:
    gamma = None
    depth = np.zeros((ROWS, COLS), dtype=np.uint8)
    temp_depth = None
    kinectThread = None
    threadActive = False    # is thread activated
    kinectActive = False    # is kinect on

    matrixIdx = 0
    matrixQueue = [0, 0, 0, 0, 0]

    def __init__(self, rows=ROWS, cols=COLS):
        self.rows = rows
        self.cols = cols
        self.make_gamma()
        self.getDepth()
        self.kinectThread = threading.Thread(target=self.depthThread)
        self.kinectThread.start()
    def depthThread(self):
        print("키넥트 스레드 시작")
        while True:
            if self.threadActive:
                #print("Getting depth...")
                self.getDepth()
                #print(self.depth)
                time.sleep(0.0001)
            else:
                print("키넥트 스레드 비활성화")
                time.sleep(3)
        print("키넥트 스레드 종료")
    def threadActivate(self, Act = True):
        if Act == True:
            print("키넥트 스레드 활성화")
            self.threadActive = True
        else:
            self.threadActive = False
            #self.kinectThread = None
    def make_gamma(self):
        """
        Create a gamma table
        """
        num_pix = 2048 # there's 2048 different possible depth values
        npf = float(num_pix)
        _gamma = np.empty((num_pix, 3), dtype=np.uint16)
        for i in range(num_pix):
            v = i / npf
            v = pow(v, 3) * 6
            pval = int(v * 6 * 256)
            lb = pval & 0xff
            pval >>= 8
            if pval == 0:
                a = np.array([255, 255 - lb, 255 - lb], dtype=np.uint8)
            elif pval == 1:
                a = np.array([255, lb, 0], dtype=np.uint8)
            elif pval == 2:
                a = np.array([255 - lb, lb, 0], dtype=np.uint8)
            elif pval == 3:
                a = np.array([255 - lb, 255, 0], dtype=np.uint8)
            elif pval == 4:
                a = np.array([0, 255 - lb, 255], dtype=np.uint8)
            elif pval == 5:
                a = np.array([0, 0, 255 - lb], dtype=np.uint8)
            else:
                a = np.array([0, 0, 0], dtype=np.uint8)
            _gamma[i] = a
        self.gamma = _gamma
        return _gamma
    def getDepth(self):
        #self.depth = np.zeros((ROWS,COLS),dtype=np.uint8)
        self.temp_depth = np.rot90(get_depth()[0])
        for row in range(len(self.depth)):
            for col in range(len(self.depth[0])):
                #print("row:{}, col:{}, indexing from {}:{}, {}:{}".format(row, col, int(row * ROW_DIV), int((row + 1) * ROW_DIV), int(col * COL_DIV), int((col + 1) * COL_DIV)))
                self.depth[row][col] = self.temp_depth[int(row * ROW_DIV):int((row + 1) * ROW_DIV), int(col * COL_DIV):int((col + 1) * COL_DIV)].mean() / 8
                self.depth[row][col] = np.bitwise_xor(self.depth[row][col], 255)
        
        self.depth[(self.depth >= 0) & (self.depth < 32)] = 0
        self.depth[(self.depth >= 32) & (self.depth < 56)] = 32
        self.depth[(self.depth >= 56) & (self.depth < 72)] = 56
        self.depth[(self.depth >= 72) & (self.depth < 88)] = 72
        self.depth[(self.depth >= 88) & (self.depth < 96)] = 88
        self.depth[(self.depth >= 96) & (self.depth < 104)] = 96
        self.depth[(self.depth >= 104) & (self.depth < 112)] = 104
        self.depth[(self.depth >= 112) & (self.depth < 120)] = 112
        self.depth[(self.depth >= 120) & (self.depth < 128)] = 120
        self.depth[(self.depth >= 128) & (self.depth < 136)] = 128
        self.depth[(self.depth >= 136) & (self.depth < 144)] = 136
        self.depth[(self.depth >= 144) & (self.depth < 152)] = 144
        self.depth[(self.depth >= 152) & (self.depth < 160)] = 152
        self.depth[(self.depth >= 160) & (self.depth < 168)] = 160
        self.depth[(self.depth >= 168) & (self.depth < 184)] = 168
        self.depth[(self.depth >= 184) & (self.depth < 200)] = 184
        self.depth[(self.depth >= 200) & (self.depth < 224)] = 200
        self.depth[(self.depth >= 224) & (self.depth < 256)] = 224

        #print(self.depth[row][col])
        #self.depth[row][col] = self.depth[row][col].invert()
        #print(self.temp_depth[row * ROW_DIV:(row + 1) * ROW_DIV,col * COL_DIV:(col + 1) * COL_DIV])

        





if __name__ == "__main__":
    k = Kinect()
    print("k.temp_depth")
    print(k.temp_depth)
    print("k.depth")
    print(k.depth)
    k.threadActivate()
    while(True):
        print("뎁스")
        print(k.depth)
        time.sleep(0.5)
