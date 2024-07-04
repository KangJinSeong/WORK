'''
Date: 2024.02.21
Title: 3차원해수유동 GPS 관련 함수
By: Kang Jin seong
'''


from Subpy import config
from Subpy import L76X
# import config   #단독으로 설정할떄
# import L76X #단독으로 설정할때
import time


x=L76X.L76X()
x.L76X_Set_Baudrate(9600)
x.L76X_Send_Command(x.SET_NMEA_BAUDRATE_115200)
time.sleep(2)
x.L76X_Set_Baudrate(115200)



class GPS_HAT:
    def __init__(self):
        '''
        TM_Repeater 와 GPS Module간의 통신을 위한 클래스\r\n
        '''
        self.x=L76X.L76X()
        self.x.L76X_Set_Baudrate(9600)
        self.x.L76X_Send_Command(x.SET_NMEA_BAUDRATE_115200)
        time.sleep(2)
        self.x.L76X_Set_Baudrate(115200)
        self.lattidue = 0
        self.longitude = 0 
    def get_data(self):
        '''
        GPS Moudle을 통한 위도 경도를 산출하는 함수\r\n
        
         _Input: None
         _Return(float): Lattidue, Longtidue
        '''
        data = self.x.L76X_Gat_GNRMC()
        data = data.decode(encoding='ISO-8859-1')
        answer = data.split('\r\n')
        for i in answer:
            if '$GNRMC' in i:
                result = i.split(',')[1:]
                for i,r in zip(result, result[1:]):
                    if r == 'N':
                        self.lattidue = float(i[:2]) + float(i[2:])/60   #위도
                    if r == 'E':
                        self.longitude = float(i[:3]) + float(i[3:])/60  #경도
                return self.lattidue, self.longitude 


if __name__ == "__main__":
    print('GPS START')
    A = GPS_HAT()
    while True:
        print(A.get_data())
