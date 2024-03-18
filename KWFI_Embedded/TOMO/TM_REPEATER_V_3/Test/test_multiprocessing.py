import time
from multiprocessing import Process, Queue

class A:
    def __init__(self):
        self.a = 0
        self.b = 0
    
    def Core1(self):
        while True:
            for i in range(0,99):
                self.a += 1
                time.sleep(0.5)
                print(f'Core1 {self.a}')
    
    def Core2(self):
        while True:
            print(f'Core2 {self.a}')
            time.sleep(0.5)


if __name__=='__main__':
    A = A()
    p1 = Process(target=A.Core1, args=())
    p2 = Process(target=A.Core2, args=())

    p1.start()
    p2.start()

    p1.join()
    p2.join()


