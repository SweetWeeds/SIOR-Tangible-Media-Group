import numpy as np
import sys
import threading
from freenect import sync_get_depth as get_depth
import time

disp_size = (640, 480)
ROWS = 10
COLS = 10

ROW_DIV = disp_size[0] / ROWS
COL_DIV = disp_size[1] / COLS

class Kinect:
    gamma = None
    depth = None
    temp_depth = None
    kinectThread = None
    threadActive = False    # is thread activated
    kinectActive = False    # is kinect on
    def __init__(self, rows=ROWS, cols=COLS):
        self.rows = rows
        self.cols = cols
        self.make_gamma()
        self.getDepth()
        self.kinectActive = True
    def depthThread(self):
        while self.threadActive:
            print("Getting depth...")
            self.getDepth()
            print(self.depth)
            time.sleep(0.005)
    def threadActivate(self, Act = True):
        print("thread activate")
        if Act == True:
            self.threadActive = True
            self.kinectThread = threading.Thread(target = self.depthThread)
            self.kinectThread.start()
        else:
            self.threadActive = False
            self.kinectThread = None
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
        self.depth = np.zeros((ROWS,COLS),dtype=np.uint8)
        self.temp_depth = np.rot90(get_depth()[0])
        for row in range(len(self.depth)):
            for col in range(len(self.depth[0])):
                #print("row:{}, col:{}, indexing from {}:{}, {}:{}".format(row, col, int(row * ROW_DIV), int((row + 1) * ROW_DIV), int(col * COL_DIV), int((col + 1) * COL_DIV)))
                self.depth[row][col] = self.temp_depth[int(row * ROW_DIV):int((row + 1) * ROW_DIV), int(col * COL_DIV):int((col + 1) * COL_DIV)].mean()
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
