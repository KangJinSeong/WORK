'''
Date: 2023.03.13
Title: 3차원해수유동 TRX_Controller 스위치 관련 SW
By: Kang Jin seong
'''

import RPi.GPIO as GPIO

class TRX_Power_switch:
    def __init__(self):
        self.SWEN = 24
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.SWEN, GPIO.OUT)
        GPIO.output(self.SWEN, False)
        GPIO.setwarnings(False)

    def main(self,s):
        if s:
            GPIO.output(self.SWEN, True)
        else:
            GPIO.output(self.SWEN, False)


if __name__ == "__main__":
    print('TRX_Power_Switch Start')
    A = TRX_Power_switch()
    try:
        A.main(0)
    except Exception as e:
        pass           
