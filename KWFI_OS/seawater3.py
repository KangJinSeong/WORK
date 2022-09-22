# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file '3chawon.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

import multiprocessing
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import pyqtgraph
from pyqtgraph.Qt import qWait
import serial
import time
from multiprocessing import Process
import sys
from pyqtgraph import PlotWidget
import numpy as np
import io
import serial.tools.list_ports
import binascii
from collections import deque
import pickle
import asyncio

ports = list(serial.tools.list_ports.comports())
temp = deque()
cnt = 0


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(935, 802)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        icon = QIcon()
        icon.addFile(u"kyungwon.png", QSize(), QIcon.Normal, QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_2 = QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.widget = PlotWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy1)
        self.gridLayout = QGridLayout(self.widget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalSpacer_3 = QSpacerItem(588, 81, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_3, 0, 0, 1, 1)


        self.verticalLayout_6.addWidget(self.widget)


        self.gridLayout_2.addLayout(self.verticalLayout_6, 0, 1, 2, 1)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setSizeConstraint(QLayout.SetMinAndMaxSize)
        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        sizePolicy2 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy2)
        self.verticalLayout_3 = QVBoxLayout(self.groupBox)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_3 = QLabel(self.groupBox)
        self.label_3.setObjectName(u"label_3")
        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy3)
        self.label_3.setMinimumSize(QSize(5, 0))
        self.label_3.setPixmap(QPixmap(u"blackcheck.png"))
        self.label_3.setScaledContents(False)

        self.horizontalLayout_6.addWidget(self.label_3)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer)

        self.pushButton_4 = QPushButton(self.groupBox)
        self.pushButton_4.setObjectName(u"pushButton_4")
        icon1 = QIcon()
        icon1.addFile(u"save.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_4.setIcon(icon1)

        self.horizontalLayout_6.addWidget(self.pushButton_4)


        self.verticalLayout_3.addLayout(self.horizontalLayout_6)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.lineEdit = QLineEdit(self.groupBox)
        self.lineEdit.setObjectName(u"lineEdit")
        sizePolicy4 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.lineEdit.sizePolicy().hasHeightForWidth())
        self.lineEdit.setSizePolicy(sizePolicy4)
        self.lineEdit.setMaximumSize(QSize(16777215, 16777204))

        self.horizontalLayout.addWidget(self.lineEdit)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_2.addWidget(self.label_2)

        self.comboBox_2 = QComboBox(self.groupBox)
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.setObjectName(u"comboBox_2")

        self.horizontalLayout_2.addWidget(self.comboBox_2)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.radioButton = QRadioButton(self.groupBox)
        self.radioButton.setObjectName(u"radioButton")

        self.horizontalLayout_3.addWidget(self.radioButton)

        self.radioButton_2 = QRadioButton(self.groupBox)
        self.radioButton_2.setObjectName(u"radioButton_2")
        self.radioButton_2.setChecked(True)

        self.horizontalLayout_3.addWidget(self.radioButton_2)

        self.pushButton = QPushButton(self.groupBox)
        self.pushButton.setObjectName(u"pushButton")

        self.horizontalLayout_3.addWidget(self.pushButton)

        self.pushButton_2 = QPushButton(self.groupBox)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.horizontalLayout_3.addWidget(self.pushButton_2)


        self.verticalLayout.addLayout(self.horizontalLayout_3)


        self.verticalLayout_3.addLayout(self.verticalLayout)


        self.verticalLayout_4.addWidget(self.groupBox)

        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setSizeConstraint(QLayout.SetFixedSize)
        self.scrollArea_2 = QScrollArea(self.centralwidget)
        self.scrollArea_2.setObjectName(u"scrollArea_2")
        sizePolicy3.setHeightForWidth(self.scrollArea_2.sizePolicy().hasHeightForWidth())
        self.scrollArea_2.setSizePolicy(sizePolicy3)
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollAreaWidgetContents_2 = QWidget()
        self.scrollAreaWidgetContents_2.setObjectName(u"scrollAreaWidgetContents_2")
        self.scrollAreaWidgetContents_2.setGeometry(QRect(0, 0, 297, 581))
        self.verticalLayout_5 = QVBoxLayout(self.scrollAreaWidgetContents_2)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.label_4 = QLabel(self.scrollAreaWidgetContents_2)
        self.label_4.setObjectName(u"label_4")
        sizePolicy4.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy4)
        self.label_4.setAlignment(Qt.AlignCenter)

        self.verticalLayout_5.addWidget(self.label_4)

        self.plainTextEdit = QPlainTextEdit(self.scrollAreaWidgetContents_2)
        self.plainTextEdit.setObjectName(u"plainTextEdit")
        sizePolicy5 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.plainTextEdit.sizePolicy().hasHeightForWidth())
        self.plainTextEdit.setSizePolicy(sizePolicy5)
        self.plainTextEdit.setMaximumSize(QSize(16777215, 30))

        self.verticalLayout_5.addWidget(self.plainTextEdit)

        self.label_5 = QLabel(self.scrollAreaWidgetContents_2)
        self.label_5.setObjectName(u"label_5")
        sizePolicy4.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy4)
        self.label_5.setAlignment(Qt.AlignCenter)

        self.verticalLayout_5.addWidget(self.label_5)

        self.textBrowser_2 = QTextBrowser(self.scrollAreaWidgetContents_2)
        self.textBrowser_2.setObjectName(u"textBrowser_2")
        sizePolicy6 = QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Minimum)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.textBrowser_2.sizePolicy().hasHeightForWidth())
        self.textBrowser_2.setSizePolicy(sizePolicy6)
        self.textBrowser_2.setMinimumSize(QSize(0, 450))

        self.verticalLayout_5.addWidget(self.textBrowser_2)

        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_2)

        self.verticalLayout_7.addWidget(self.scrollArea_2)


        self.verticalLayout_4.addLayout(self.verticalLayout_7)


        self.gridLayout_2.addLayout(self.verticalLayout_4, 0, 0, 2, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 935, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Kyungwon", None))
        self.groupBox.setTitle("")
        self.label_3.setText("")
        self.pushButton_4.setText("")
        self.label.setText(QCoreApplication.translate("MainWindow", u"Baud Rate", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Port", None))
        for i in range(len(ports)):
            self.comboBox_2.setItemText(i, QCoreApplication.translate("MainWindow", u"{}".format(ports[i][0]), None))


        self.radioButton.setText(QCoreApplication.translate("MainWindow", u"HEX", None))
        self.radioButton_2.setText(QCoreApplication.translate("MainWindow", u"ASCII", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Connection", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"DisConnection", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"TX DATA", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"RX DATA", None))
    # retranslateUi

class MyWindow(QMainWindow,Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.pushButton.clicked.connect(self.connSerial)
        self.pushButton_2.clicked.connect(self.disconnSerial)
        self.pushButton_4.clicked.connect(self.save_file)
    
    def connSerial(self):# Serial 연결
        self.ser = serial.Serial(self.comboBox_2.currentText(),int(self.lineEdit.text()),timeout=0.1)
        self.sio = io.TextIOWrapper(io.BufferedRWPair(self.ser,self.ser))

        self.label_3.setPixmap('red_check.jpg')
        if self.plainTextEdit.toPlainText() == '':
            self.label_3.setPixmap('blackcheck.png')
            self.Qmessage = QMessageBox()
            self.waring_event()
            self.ser.close()
            self.timer.stop()
            MyWindow()
        else:
            if self.radioButton.isChecked(): # str -> hex
                self.sio.write(''.join(list(map(hex,[int(('{}{}').format('0x',i),16) for i in (self.plainTextEdit.toPlainText().split(' '))]))))
            elif self.radioButton_2.isChecked(): # str -> ascii
                self.sio.write(''.join(list(map(chr,[int(('{}{}').format('0x',i),16) for i in (self.plainTextEdit.toPlainText().split(' '))]))))
        self.sio.flush()
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.connectSerial)
        self.timer.start()
    
    def waring_event(self): # 경고창
        return self.Qmessage.warning(self,'Error','전송 메세지를 입력해주세요')

    def connectSerial(self):
        global cnt

        # if self.radioButton.isChecked(): # str -> hex
        #     self.res = binascii.hexlify(bytes(self.sio.readline()[:-1],'utf-8')).decode()
        # elif self.radioButton_2.isChecked(): # str -> ascii
        #     self.res = ''.join(str(ord(i)) for i in self.sio.readline()[:-1])
        self.res = self.sio.readline()
        # self.sio.flush()

        if self.res!='':
            cnt = 0
            temp.append(self.res)
            if len(temp)%1000 == 0:
                self.loop = asyncio.get_event_loop()
                self.loop.run_until_complete(self.rx_transmitter())
                self.loop.close()
        else:
            cnt+=1
            if cnt == 5:
                self.loop.run_until_complete(self.rx_transmitter())
                self.loop.close()

                self.label_3.setPixmap('blackcheck.png')
                cnt = 0



        self.textBrowser_2.append(str(self.res))
    
    def disconnSerial(self):
        self.label_3.setPixmap('blackcheck.png')

        if self.timer.isActive() == True:
            # self.textBrowser_2.clear()# textbrowser 표시 값 삭제

            self.ser.close()
            self.timer.stop()
    
    def save_file(self): # 데이터 저장
        save = QFileDialog.getSaveFileName(None,'Save File',"./","All files (*.*);;")
        textedit = QTextEdit('{}'.format(temp))

        with open(save[0],'w',encoding='utf-8') as f:
            text = textedit.toPlainText()
            f.write(text)
        temp.clear()
        f.close()
    
    def sleep(self,n):
        qWait(n*1000)
    
    def rx_transmitter(self):
        self.widget.clear()
        pen = pyqtgraph.mkPen(color=(255,0,0),width=4)
        self.data_line = self.widget.plot([i for i in range(len(temp))],list(map(float,temp)),pen=pen)
        # await asyncio.sleep(1)
        # self.sleep(1)
        return self.widget.addItem(self.data_line)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    target=window.show()
    app.exec_()