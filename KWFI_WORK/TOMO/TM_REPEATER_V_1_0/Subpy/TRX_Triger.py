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

    def Data_analysis(self, data):  # data: 문자열 Mqtt로부터 수신 받은 데이터
        Data = data.split(',')
        print(Data)

        if ('START' in Data):
            result = [int(i) for i in Data[1:-1]]
        else:
            result = [24,60,60,100]
        return result 

    def main(self):
        while True:
            if (self.s_hour%24) == datetime.now().hour:
                if (self.s_min%60) == datetime.now().minute:
                    print(self.s_hour, self.s_min, self.s_interval, self.s_id)
                    if self.s_min + self.s_interval == 60:
                        self.s_hour = self.s_hour + 1
                    
                    self.s_min = datetime.now().minute
                    print(self.s_hour, self.s_min, self.s_interval, self.s_id)
                    '''
                    DSP 통신을 통한 TXID RS232 통신 코드 작성
                    '''
                    print('TRX_Triger START')
                    print(datetime.now().hour, datetime.now().minute)
                    time.sleep(3)
                    GPIO.output(self.TXEN, True)
                    time.sleep(0.2)
                    GPIO.output(self.TXEN, False)
                    
                    break



if __name__ == "__main__":
    print('TRX_Triger ON')
    A = TRX_TRG()
    try:
        A.timezone(hour = 11,min = 57,interval = 1,id = 1,state = 1)
        A.main()
 
        A.timezone(hour = 11,min = 57,interval = 2,id = 1,state = 1)

    except Exception as e:
        pass           
