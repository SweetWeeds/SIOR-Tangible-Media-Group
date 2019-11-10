import pyaudio
import numpy as np
import threading

CHUNK = 2**11
RATE = 44100

ROWS = 10
COLS = 10

MAX = 50 * 17000 / 2 ** 16

class AudioSpectrum:
    p = None
    stream = None
    plot2D = [0] * int(np.sqrt(ROWS / 2 ** 2 + COLS / 2 ** 2))
    plot3D = np.zeros((ROWS,COLS),dtype=np.uint8)
    threadActive = False
    def __init__(self):
        self.p=pyaudio.PyAudio()
        self.stream=self.p.open(format=pyaudio.paInt16,channels=1,rate=RATE,input=True,
              frames_per_buffer=CHUNK)
    def audioThread(self):
        while(threadActive):
            self.update3D()
    def threadActivate(self, Act = True):
        if threadActive == True and Act == True:
            return
        elif threadActive == False and Act == True:
            self.threadActive = True
            self.audioThread = threading.Thread(target = self.audioThread)
            self.audioThread.start()
        else:
            self.threadActive = False
            self.audioThread = None
    def update(self):
        data = np.fromstring(self.stream.read(CHUNK),dtype=np.int16)
        peak = np.average(np.abs(data)) * 2
        bars = int(50*peak/2**10)
        self.plot2D.pop()
        self.plot2D.insert(0, bars)
    def update3D(self):
        self.update()
        width = ROWS / 2
        height = COLS / 2
        for i in range(width):
            for j in range(height):
                idx = int(np.sqrt((i ** 2) + (j ** 2)))
                self.plot3D[width + i][height + j] = self.plot2D[idx]
                self.plot3D[width + i][height -1 - j] = self.plot2D[idx]
                self.plot3D[width -1 - i][height + j] = self.plot2D[idx]
                self.plot3D[width -1 - i][height -1 - j] = self.plot2D[idx]        
    def Close(self):
        self.stream.top_stream()
        self.stream.close()
        self.p.terminate()

if __name__ == "__main__":
    a = AudioSpectrum()
    while(True):
        #os.system('clear')
        self.update3D()
        print(self.plot3D)
    a.Close()