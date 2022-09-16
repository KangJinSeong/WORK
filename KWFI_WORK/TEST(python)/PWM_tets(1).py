import RPi.GPIO as GPIO
import time
import pigpio



PI = pigpio.pi()
PI.hardware_PWM(13,0,500000)

t = 1/1000000
p = 0
while p < 50:
    
    p += 1
    f = 430000
    for i in range(100):
        
        PI.hardware_PWM(13,f,500000)
        f += 400
        a = PI.get_current_tick()
        time.sleep(t)
        b = PI.get_current_tick()
#         print(b-a)
#         print(f)
    print(b-a)
        
    PI.hardware_PWM(13,0,500000)
    time.sleep(1)

PI.stop()
# PI.hardware_PWM(13,30000,500000)
