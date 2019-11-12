from Matrix import *
from Kinect import *
from Audio import *
import threading
import time

ROWS = 3
COLS = 10

def mainThread(k,m):
    while(True):
        k.getDepth()
        #print(a.plot3D)
        m.setKinectHeight(k.depth)
        time.sleep(0.0001)

if __name__=="__main__":
    k = Kinect()
    #a = AudioSpectrum()
    #a.threadActivate()
    m = Matrix(ROWS, COLS)
    m.syncActivate()
    t = threading.Thread(target = mainThread, args=(k,m))
    t.start()
