'''
Date: 2023.03.13
Title: 3차원해수유동 시간의 따른 Triger 신호 출력 관련 SW
By: Kang Jin seong
'''

import RPi.GPIO as GPIO
import time
from datetime import datetime
from Subpy import UART_V_1_0
import paho.mqtt.publish as publish
import os
# import UART_V_1_0   #TEST
# import TRX_Controller_Swtich    #TEST

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
        self.UARTIP = UART_V_1_0.UART_HAT()
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
            result = [0,0,0,0]
        return result 
        
    def main(self, stationid):
        if (self.s_hour%24) == datetime.now().hour:
            if (self.s_min%60) == datetime.now().minute:
                if self.s_min + self.s_interval == 60:
                    self.s_hour = self.s_hour + 1
                
                self.s_min = datetime.now().minute
                # test code
                # self.timezone(hour = self.s_hour,min = self.s_min + self.s_interval,interval = 4,id = 2)
  
                FPGA_TX = ''.join([chr(i) for i in [0x3E,0x35,0x53,int(hex(ord(str(self.s_id))),16),0x0D]])

                while True:
                    self.UARTIP.FPGA_Put_TX(FPGA_TX)
                    print('FPGA_TX:', FPGA_TX)
                    data = self.UARTIP.FPGA_ECO_Dat_analysis()
                    print('ECO DATA:', data)
                    if data == FPGA_TX:     # Test !=
                        print('TRX_Triger START')
                        time.sleep(1)
                        GPIO.output(self.TXEN, True)
                        time.sleep(1.1)
                        GPIO.output(self.TXEN, False)
                        for i in range(2):
                            trash_data = self.UARTIP.FPGA_Dat_analysis()
                            print('Trash_data :',trash_data)
                        break
                    
                while (int(stationid) != self.s_id):  #수신 모드 일때
                    print('RX Data ing')
                    data = self.UARTIP.FPGA_Dat_analysis()
                    print('FPGA_GET data:',data)
                    if len(data) > 0:
                        if data[0] == '(':
                            data_answer = data.replace(')(', ',')
                            data_answer = data_answer[1:-1]

                            Pico_data = self.UARTIP.PICO_Dat_analysis()
                            print(type(stationid), type(Pico_data), type(data_answer))
                            FPGA_Temp_data = self.UARTIP.FPGA_Put_Temp()

                            result = bytes(stationid,'utf-8')+b','+[Pico_data[1:] if b'\x00' in Pico_data else Pico_data][0]+b',' + bytes(FPGA_Temp_data,'utf-8')+b','+bytes(data_answer,'utf-8')
                            print('RX Data:', result)
       
                            publish.single(topic='Core/sendTestData1234/data',payload = result,hostname='test.mosquitto.org',keepalive= 0)
                            break


if __name__ == "__main__":
    print('TRX_Triger ON')
    
    # B = TRX_Controller_Swtich.TRX_Power_switch()
    # B.main(0)
    # time.sleep(2)
    # B.main(1)
    # time.sleep(60)

    A = TRX_TRG()

    A.timezone(hour = 13,min = 34,interval = 4,id = 2)
    while True:
        A.main(1)
         
