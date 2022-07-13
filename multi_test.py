import os 
from multiprocessing import Process, Queue
import time

def f(q, name):
    num = 0
    while True:
        q.put(num)
        print('pid of parent:', os.getppid()) 
        print('pid of %s : %d' %(name, os.getpid())) 
        print(num)
        num += 1
        if num == 100:
            num = 0
        time.sleep(0.5)

def m(q, name):
   while True:
    print('pid of parent:', os.getppid()) 
    print('pid of %s : %d' %(name, os.getpid())) 
    print('%d' %q.get())
    time.sleep(1)

if __name__ == '__main__': 
    # print('pid of main:', os.getpid()) 
    q = Queue()
    p1 = Process(target=f, args=(q,'proc_1')) 
    p2 = Process(target=m, args=(q,'proc_2'))
    p1.start()
    p2.start()

