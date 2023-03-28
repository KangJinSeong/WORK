'''
Date: 2023.03.28
Title: TM_Repeater SWITCH B/D 제어 관련 함수
By: Kang Jin seong
'''
import RPi.GPIO as GPIO # 라즈베리파이 포트 제어 관련 모듈

class TRX_Power_switch:
    def __init__(self): # 클래스 함수 초기 설정 값 선언 
        self.SWEN = 24  # Pin18  (A1.1.4 SWITCH B/D 회로도 J34 커넥터 핀맵)
        GPIO.setmode(GPIO.BCM)  # GPIO 핀 모드 (BCM)
        GPIO.setup(self.SWEN, GPIO.OUT) # GPIO 출력모드
        GPIO.output(self.SWEN, False)   # GPIO 초기값 0
        GPIO.setwarnings(False) # GPIO Warnings 출력 해제
    def main(self,s):   # TRX_Controller 전원 공급 관련 스위치 함수
        if s:
            GPIO.output(self.SWEN, True)    # GPIO 출력 High
        else:
            GPIO.output(self.SWEN, False)   # GPIO 출력 LOW
