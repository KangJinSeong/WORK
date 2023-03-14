'''
Date: 2023.03.13
Title: 3차원해수유동 GPS 
By: Kang Jin seong
'''

from Subpy import config
from Subpy import L76X
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
    def get_data(self):
        data = self.x.L76X_Gat_GNRMC()
        data = data.decode()
        answer = data.split('\r\n')
        for i in answer:
            if '$GNRMC' in i:
                result = i.split(',')[1:]
                for i,r in zip(result, result[1:]):
                    if r == 'N':
                        lattidue = float(i[:2]) + float(i[2:])/60   #위도
                    if r == 'E':
                        longitude = float(i[:3]) + float(i[3:])/60  #경도

        return lattidue, longitude

    def main(self):
        lat,lon = self.get_data()
        lat = '{:0.8f}'.format(lat)
        lon = '{:0.8f}'.format(lon)
        print(lat, lon)
        return lat, lon

if __name__ == "__main__":
    print('GPS START')
    A = GPS_HAT()
    try:
        A.main()
    except Exception as e:
        pass