import time
from machine import ADC,Pin

class MUX:
    def __init__(self):
        self.SELA = 0#핀 초기 설정 값 0번은 LOW 1번은 HIGH
        self.SELB = 0#핀 초기 설정 값
        self.SELC = 0#핀 초기 설정 값
        self.DSPON = 1#핀 초기 설정 값
        self.TRXON = 1#핀 초기 설정 값
        self.TRXCON = 1#핀 초기 설정 값
       
        self.sela = Pin(10,mode=Pin.OUT,value=self.SELA) # SELA와 연동된 GPIO
        self.selb = Pin(11,mode=Pin.OUT,value=self.SELB) # SELB와 연동된 GPIO
        self.selc = Pin(12,mode=Pin.OUT,value=self.SELC) # SELC와 연동된 GPIO
    
    def MUX_CHECK(self,outputV=0.0,limit=0.0,Err_check=0):#Err_check : 0 data_read, 1 err
        
        self.err_check = Err_check
        self.MNT = ADC(26) # MNT와 연동된 GPIO ADC로 인가 12bit 출력 0~65535
        
        if self.err_check == 0:
            self.dspon = Pin(6,mode=Pin.OUT,value=self.DSPON)#DSPON과 연동된 GPIO
            self.trxon = Pin(7,mode=Pin.OUT,value=self.TRXON)#TRXPON과 연동된 GPIO
            self.trxcon = Pin(8,mode=Pin.OUT,value=self.TRXCON)#TRXCON과 연동된 GPIO
            DSPEN = 0#초기 설정 값
            TRXPSEN = 0#초기 설정 값
            TRXCSEN = 0#초기 설정 값
            DC12VMNT = 0#초기 설정 값
            time.sleep(0.5)
            while True:
                self.MNTIN = (3.3/65536)*self.MNT.read_u16() #MNT 인가 전압 계산 3.3/65536*인가비트
                if self.MNTIN>=outputV:
                    DATA = ADC(28)#ADA가 연동된 GPIO ADC로 인가 12BIT 출력 0~65535
                    DSPEN = (3.3/65536)*DATA.read_u16() # VALUE가 0일 때 DSPEN출력
                    if DSPEN>=limit:# DSPEN 값이 한계전압보다 높을 때
                        self.Break_DT() # 정지 신호 메서드
                        DSPEN,TRXPSEN,TRXCSEN,DC12VMNT,self.err_check = 0,0,0,0,1#데이터 반환
                        break
                    time.sleep(0.1)
                    Pin(10,mode=Pin.OUT,value=1)#SELA에 1인가
                    TRXPSEN = (3.3/65536)*DATA.read_u16()#VLAUE가 1일 때 TRXPSEN 출력
                    if TRXPSEN>=limit:# TRXPSEN 값이 한계전압보다 높을 때
                        self.Break_DT()# 정지 신호 메서드
                        DSPEN,TRXPSEN,TRXCSEN,DC12VMNT,self.err_check = 0,0,0,0,1#데이터 반환
                        break
                    time.sleep(0.1)
                    DATA = ADC(27)#ADB가 연동된 GPIO ADC로 인가 12BIT 출력 0~65535
                    TRXCSEN = (3.3/65536)*DATA.read_u16()#VALUE가 0일 때 TRXCSEN 출력
                    if TRXCSEN>=limit:#TRXCSEN 값이 한계 전압보다 높을 때
                        self.Break_DT()# 정지 신호 메서드
                        DSPEN,TRXPSEN,TRXCSEN,DC12VMNT,self.err_check = 0,0,0,0,1#데이터 반환
                        break
                    Pin(11,mode=Pin.OUT,value=1)#SELB에 1인가
                    time.sleep(0.1)
                    DC12VMNT = (12/65536)*DATA.read_u16()#VALUE가 1일 때 DC12VMNT 출력 해당 같은 경우 12V로 출력 하기 때문에 12로 계산
                    break
            
            return DSPEN,TRXPSEN,TRXCSEN,DC12VMNT,self.MNTIN,self.err_check # 데이터 반환
        else:
            while True:#ERROR데이터가 1이 들어왔을 때
                self.MNTIN = (3.3/65536)*self.MNT.read_u16()#MNT와 연동된 GPIO ADC로 인가 12BIT 출력 0~65535
                if self.MNTIN>=outputV:
                    break
                time.sleep(0.5)
            return 0,0,0,0,self.MNTIN,1#데이터 반환
        
    def Break_DT(self):#정지 신호 메서드
        stop_dat = [self.dspon,self.trxon,self.trxcon]#DSPON,TRXON,TRXCON GPIO
        
        for i in stop_dat:
            i.value(0)#해당 VLAUE값을 0으로 변경
                
if __name__=='__main__':
    print(MUX().MUX_CHECK(outputV=1.0,limit=2,Err_check=0))
