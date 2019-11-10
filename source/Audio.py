import pyaudio
import numpy as np
import os

CHUNK = 2**11
RATE = 44100
"""
p=pyaudio.PyAudio()
stream=p.open(format=pyaudio.paInt16,channels=1,rate=RATE,input=True,
              frames_per_buffer=CHUNK)

for i in range(int(10*44100/1024)): #go for a few seconds
    data = np.fromstring(stream.read(CHUNK),dtype=np.int16)
    peak=np.average(np.abs(data))*2
    bars="#"*int(50*peak/2**16)
    print("%04d %05d %s"%(i,peak,bars))

stream.stop_stream()
stream.close()
p.terminate()
"""
MAX = 50 * 17000 / 2 ** 16
ROWS = 10
COLS = 10

class AudioSpectrum:
    p = None
    stream = None
    plot2D = [0] * int(np.sqrt(ROWS ** 2 + COLS ** 2))
    plot3D = np.zeros((ROWS,COLS),dtype=np.uint8)
    def __init__(self):
        self.p=pyaudio.PyAudio()
        self.stream=self.p.open(format=pyaudio.paInt16,channels=1,rate=RATE,input=True,
              frames_per_buffer=CHUNK)
    def test(self):
        while(True):
            #os.system('clear')
            self.update3D()
            print(self.plot3D)
    def update(self):
        data = np.fromstring(self.stream.read(CHUNK),dtype=np.int16)
        peak = np.average(np.abs(data)) * 2
        bars = int(50*peak/2**13)
        self.plot2D.pop()
        self.plot2D.append(0, bars)
    def update3D(self):
        self.update()
        width = ROWS / 2
        height = COLS / 2
        for i in range(width):
            for j in range(height):
                idx = int(np.sqrt(((width - i) ** 2) + ((height -j) ** 2)))
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
    a.test()
    a.Close()