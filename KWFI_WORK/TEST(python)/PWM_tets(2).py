import RPi.GPIO as GPIO
import pigpio
import time
PI = pigpio.pi()

# PI.hardware_PWM(13,430000,500000)

usleep = lambda x: time.sleep(x/1000000.0)

while True:
    t1 = time.time()
#     time.sleep(0.000001)
    usleep(1)
    t2 = time.time()
    print(t2-t1)

    