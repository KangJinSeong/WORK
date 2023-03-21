'''
Date: 2023.03.13
Title: 3차원해수유동 시간의 따른 Triger 신호 출력 관련 SW
By: Kang Jin seong
'''

import RPi.GPIO as GPIO
import time
from datetime import datetime
from Subpy import UART_V_1_0
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
                '''
                DSP 통신을 통한 TXID RS232 통신 코드 작성
                '''

                FPGA_TX = ''.join([chr(i) for i in [0x3E,0x35,0x53,int(hex(ord(str(self.s_id))),16),0x0D]])
                self.UARTIP.FPGA_Put_TX(FPGA_TX)
                print('FPGA_TX:', FPGA_TX)
                data = self.UARTIP.FPGA_ECO_Dat_analysis()
                print('ECOR DATA:', data)
                if data == FPGA_TX:
                    print('TRX_Triger START')
                    time.sleep(1)
                    GPIO.output(self.TXEN, True)
                    time.sleep(1.1)
                    GPIO.output(self.TXEN, False)
                print(stationid, self.s_id)
                print(type(stationid), type(self.s_id) )
                # while (stationid != self.s_id):  #수신 모드 일때
                #     print('RX Data ing')
                #     data = self.UARTIP.FPGA_Dat_analysis()
                #     print(data)
                #     if data[0] == '(':
                #         data_answer = data.replace(')(', ',')
                #         data_answer = data_answer[1:-2]
                #         Pico_data = self.UARTIP.PICO_Dat_analysis()
                #         result = "{},{},{} ".format(stationid, Pico_data, data_answer)
                #         print('RX DAta:')
                #         print(result)
                #         break
                
                    
                    





if __name__ == "__main__":
    print('TRX_Triger ON')
    
    # B = TRX_Controller_Swtich.TRX_Power_switch()
    # B.main(1)

    A = TRX_TRG()
    try:
        A.timezone(hour = 16,min = 13,interval = 1,id = 2)
        A.main()


    except Exception as e:
        pass           
