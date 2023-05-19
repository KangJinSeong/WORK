import RPi.GPIO as GPIO
import pigpio
import time

PI = pigpio.pi()    

f = 430000
t = 1/1000000
t1 = 400*t

PI.hardware_PWM(13,f,500000)
time.sleep(t1)
# for i in range(10):
#     PI.hardware_PWM(13,f,500000)
#     f += 4000
#     time.sleep(t1)
    
PI.hardware_PWM(13,0,500000)

PI.stop()
