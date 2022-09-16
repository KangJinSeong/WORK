import time

usleep = lambda x: time.sleep(x/1000000.0)

a = time.time()
usleep(1)
b = time.time()
print(b-a)