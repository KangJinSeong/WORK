
'''
Date: 2021.08.26
Title: signal plot with multiprocess
By: Kang Jin Seong
'''

'''
reference site : https://wikidocs.net/87141
                https://codetorial.net/matplotlib/animation_funcanimation.html
'''
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from multiprocessing import Process, Queue
import multiprocessing as mp
import datetime
import time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def producer(q):
    proc = mp.current_process()
    print(proc.name)
    t = np.arange(start = 0, stop = 0.1, step = 1/(100*100))
    while True:
        for i in range(1,10):
            data = i*np.sin(2*np.pi*100*t)
            q.put(data)
            time.sleep(0.01)

class Consumer(QThread):
    
    def __init__(self, q):
        super().__init__()
        self.q = q

    def run(self):

        fig, ax = plt.subplots()
        ax.set_xlim(0,0.1);ax.set_ylim(-10,10)
        line, = ax.plot([], [])

        def animate(i):
            x = np.arange(start = 0, stop = 0.1, step = 1/(100*100))
            y = q.get()
            line.set_data(x, y)
            return line,

        anim = FuncAnimation(fig, animate, frames=500, interval=100)
        plt.show()


if __name__ == "__main__":
    q = Queue()

    # producer process
    p = Process(name="producer", target=producer, args=(q, ), daemon=True)
    p.start()

    # Main process
  
    Consumer.run(q)

