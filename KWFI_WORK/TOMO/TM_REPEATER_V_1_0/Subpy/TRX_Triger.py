'''
Date: 2023.03.13
Title: 3차원해수유동 시간의 따른 Triger 신호 출력 관련 SW
By: Kang Jin seong
'''

import RPi.GPIO as GPIO
import time
from datetime import datetime

class TRX_TRG:
    def __init__(self):
        
        self.TXEN = 22
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.TXEN, GPIO.OUT)
        GPIO.output(self.TXEN, False)
        GPIO.setwarnings(False)

        self.s_hour = 0
        self.s_min = 0
        self.s_interval = 0
        self.s_id = 0

        '''
        DSP 통신 관련 초기화 함수 작성
        '''
    def timezone(self,hour,min,interval,id):
        self.s_hour = hour
        self.s_min = min
        self.s_interval = interval
        self.s_id = id
    def main(self):
        if ((self.s_hour+12)%24) == datetime.now().hour:
            if ((self.s_min+self.s_interval)%60) == datetime.now().minute:
                self.s_min = datetime.now().minute
                '''
                DSP 통신을 통한 TXID RS232 통신 코드 작성
                '''
                print('TRX_Triger START')
                print(datetime.now().hour, datetime.now().minute)
                time.sleep(3)
                GPIO.output(self.TXEN, True)
                time.sleep(0.2)
                GPIO.output(self.TXEN, False)



if __name__ == "__main__":
    print('TRX_Triger ON')
    A = TRX_TRG()
    try:
        A.timezone(hour = 11,min = 57,interval = 1,id = 1,state = 1)
        A.main()
 
        A.timezone(hour = 11,min = 57,interval = 2,id = 1,state = 1)

    except Exception as e:
        pass           
