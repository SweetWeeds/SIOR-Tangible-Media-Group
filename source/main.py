from Matrix import *
from Kinect import *
import threading
import time

ROWS = 10
COLS = 1

def mainThread(k,m):
    while(True):
        k.getDepth()
        print(k.depth)
        m.setKinectHeight(k.depth)
        time.sleep(0.005)

if __name__=="__main__":
    k = Kinect()
    m = Matrix(ROWS, COLS)
    m.syncActivate()
    t = threading.Thread(target = mainThread, args=(k,m))
    t.start()
