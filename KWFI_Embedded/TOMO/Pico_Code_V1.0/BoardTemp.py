import utime#시간 라이브러리
from machine import I2C,Pin#I2C및Pin 통신 라이브러리
import struct#구조체 반환 라이브러리

class Board_temp:
    def __init__(self):
        self.i2c = I2C(0,sda=Pin(20),scl=Pin(21),freq=400000)#I2C 통신을 위한 함수 SDA의 경우 GPIO 20, SCL의 경우 GPIO 21번과 연결 되어있다 
        self.TEMP = 'b'
        self.devices = self.i2c.scan()#i2c 주소지를 읽기 위한 함수
        
    def read_temp(self):
        while True:
            try:
                TEMPDAT = struct.unpack(self.TEMP,self.i2c.readfrom(self.devices[0],1))[0]#readfrom으로 읽은 데이터를 bytes로 변환
                print('%s:%.1f'%('Celsius',TEMPDAT))
                utime.sleep(0.1)
            except:
                TEMPDAT = 0#에러 발생 시 0 데이터 반환
#                 print('%s:%f'%('Celsius',0.0))
                utime.sleep(0.1)
            break
        return TEMPDAT#데이터 반환

if __name__=='__main__':
    Board_temp().read_temp()            
