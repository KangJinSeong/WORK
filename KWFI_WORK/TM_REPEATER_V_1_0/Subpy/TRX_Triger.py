'''
Date: 2023.03.13
Title: 3차원해수유동 시간의 따른 Triger 신호 출력 관련 SW
By: Kang Jin seong
'''

import RPi.GPIO as GPIO
import time


class TRX_TRG:
    def __init__(self):
        self.TXEN = 22
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.TXEN, GPIO.OUT)
        GPIO.output(self.TXEN, False)
        GPIO.setwarnings(False)

    def main(self):
        GPIO.output(self.TXEN, True)
        time.sleep(0.2)
        GPIO.output(self.TXEN, False)



if __name__ == "__main__":
    print('TRX_Triger Start')
    A = TRX_TRG()
    try:
        A.main()
    except Exception as e:
        pass           
