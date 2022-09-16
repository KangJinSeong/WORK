'''
Date: 2022.06.20
Title: 
By: Kang Jin Seong
'''

#버튼 클릭으로 메시지를 발행하는 GUI 프로그램

import paho.mqtt.publish as publish
from tkinter import *

def change_color(): # 버튼 클릭 콜백 함수
    #콜백 함수는 인자를 갖지 않으므로 필요하면 글로벌 변수를 선언하여 사용한다.
    global button_bg, button_txt

    #토글 모드로 동작
    if button_bg == 'blue':
        button_bg = 'red'
        button_txt = 'ON'
    else:
        button_bg = 'blue'
        button_txt = 'OFF'

    #버튼 색상 및 텍스트 변셩
    button.configure(text = button_txt, bg = button_bg)
    #메시지 발생
    publish.single("control/LED", button_txt, hostname="test.mosquitto.org")

root = Tk()
button_bg = 'blue'
button_txt = 'OFF'

button = Button(root, text = button_txt, fg = 'yellow', font = ('Vernada', 16), bg = button_bg, command = change_color)
button.pack()
root.mainloop()
