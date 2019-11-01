import numpy as np
import sys
import threading
from freenect import sync_get_depth as get_depth

disp_size = (640, 480)
ROWS = 8
COLS = 8

ROW_DIV = disp_size[0] / ROWS
COL_DIV = disp_size[1] / COLS

class Kinect:
    gamma = None
    depth = None
    temp_depth = None
    kinectThread = None
    threadActive = False
    kinectActive = False
    def __init__(self):
        self.make_gamma()
        self.getDepth()
        self.kinectActive = True
    def threadActivate(self, Act = True):
        if Act == True:
            self.kinectThread = threading.Thread()
    def make_gamma(self):
        """
        Create a gamma table
        """
        num_pix = 2048 # there's 2048 different possible depth values
        npf = float(num_pix)
        _gamma = np.empty((num_pix, 3), dtype=np.uint16)
        for i in xrange(num_pix):
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
        self.depth = np.zeros((8,8),dtype=np.uint8)
        self.temp_depth = np.rot90(get_depth()[0])
        for row in range(len(self.depth)):
            for col in range(len(self.depth[0])):
                #print("row:{}, col:{}, indexing from {}:{}, {}:{}".format(row, col, row * ROW_DIV, (row + 1) * ROW_DIV,col * COL_DIV, (col + 1) * COL_DIV))
                self.depth[row][col] = self.temp_depth[row * ROW_DIV:(row + 1) * ROW_DIV, col * COL_DIV:(col + 1) * COL_DIV].mean() / 8
                #print(self.temp_depth[row * ROW_DIV:(row + 1) * ROW_DIV,col * COL_DIV:(col + 1) * COL_DIV])

if __name__ == "__main__":
    k = Kinect()
    print("k.temp_depth")
    print(k.temp_depth)
    print("k.depth")
    print(k.depth)