'''
Date: 2023.03.13
Title: 3차원해수유동 GPS 
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
        self.x=L76X.L76X()
        self.x.L76X_Set_Baudrate(9600)
        self.x.L76X_Send_Command(x.SET_NMEA_BAUDRATE_115200)
        time.sleep(2)
        self.x.L76X_Set_Baudrate(115200)
        self.lattidue = 0
        self.longitude = 0
    def get_data(self):
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
        self.lattidue = 0
        self.longitude = 0
        return self.lattidue, self.longitude  

    def main(self):
        lat,lon = self.get_data()

        '''
        lat, lon 데이터가 없을 경우 처리 루틴 필요
        '''

        lat = '{:0.8f}'.format(lat)
        lon = '{:0.8f}'.format(lon)


        return lat, lon

if __name__ == "__main__":
    print('GPS START')
    A = GPS_HAT()
    try:
        print(A.main())
    except Exception as e:
        pass