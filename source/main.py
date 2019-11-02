from Matrix import *
from Kinect import *
import threading
import time

ROWS = 8
COLS = 8

def mainThread(k,m):
    while(True):
        m.setHeight(k.depth)
        time.sleep(0.5)

if __name__=="__main__":
    k = Kinect()
    m = Matrix(ROWS, COLS)
    t = threading.Thread(target = mainThread, args=(k,m))
    t.start()
