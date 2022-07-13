# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'TCPSSS.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################


import PySide2
from PySide2 import QtCore
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import sys
import threading
import socket
from pyqtgraph import PlotWidget
import time
import queue
import asyncio
import pickle
from collections import deque
import pyqtgraph

Que = queue.Queue()
deq = []

tempdeq = ""
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
        self.groupBox.setMinimumSize(QSize(280, 0))
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
        self.lineEdit.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout.addWidget(self.lineEdit)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_2.addWidget(self.label_2)

        self.lineEdit_2 = QLineEdit(self.groupBox)
        self.lineEdit_2.setObjectName(u"lineEdit_2")
        sizePolicy4.setHeightForWidth(self.lineEdit_2.sizePolicy().hasHeightForWidth())
        self.lineEdit_2.setSizePolicy(sizePolicy4)
        self.lineEdit_2.setMaximumSize(QSize(16777215, 16777204))
        self.lineEdit_2.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_2.addWidget(self.lineEdit_2)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_4 = QLabel(self.groupBox)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_4.addWidget(self.label_4)

        self.lineEdit_3 = QLineEdit(self.groupBox)
        self.lineEdit_3.setObjectName(u"lineEdit_3")
        sizePolicy4.setHeightForWidth(self.lineEdit_3.sizePolicy().hasHeightForWidth())
        self.lineEdit_3.setSizePolicy(sizePolicy4)
        self.lineEdit_3.setMaximumSize(QSize(16777215, 16777204))
        self.lineEdit_3.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_4.addWidget(self.lineEdit_3)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.pushButton = QPushButton(self.groupBox)
        self.pushButton.setObjectName(u"pushButton")

        self.horizontalLayout_3.addWidget(self.pushButton)


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
        self.scrollAreaWidgetContents_2.setGeometry(QRect(0, 0, 276, 551))
        self.verticalLayout_5 = QVBoxLayout(self.scrollAreaWidgetContents_2)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.label_5 = QLabel(self.scrollAreaWidgetContents_2)
        self.label_5.setObjectName(u"label_5")
        sizePolicy4.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy4)
        self.label_5.setAlignment(Qt.AlignCenter)

        self.verticalLayout_5.addWidget(self.label_5)

        self.textBrowser_2 = QTextBrowser(self.scrollAreaWidgetContents_2)
        self.textBrowser_2.setObjectName(u"textBrowser_2")
        sizePolicy5 = QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Minimum)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.textBrowser_2.sizePolicy().hasHeightForWidth())
        self.textBrowser_2.setSizePolicy(sizePolicy5)
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
        self.lineEdit.setText(QCoreApplication.translate("MainWindow", u"", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"TCP/IP", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Port", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Trigger", None))
        self.lineEdit_3.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Connection", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"RX DATA", None))
    # retranslateUi

class MyWindow(QMainWindow,Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.Qmessage = QMessageBox()
        self.pushButton.clicked.connect(self.runTask)
    
    def runTask(self):
        self.pushButton.setDisabled(True)

        self.TCPPORT = (self.lineEdit.text(),int(self.lineEdit_2.text()))
        # TCP/IP , PORT 번호
        try:
            self.trigger = float(self.lineEdit_3.text())
        except:
            self.Qmessage.warning(self,'Error','숫자를 입력해주세요')
            self.connSocket()

        self.thread = QThread() # QTrhead 생성
        self.worker = Worker(self.TCPPORT,self.trigger) # background 인스턴스 생성

        self.worker.moveToThread(self.thread) # worker를 thread 넣기

        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        # self.worker.progress.connect(self.updateTextBrowser)
        self.worker.drawprogress.connect(self.drawgraph)

        self.thread.start() # Thread 실행

    def updateTextBrowser(self,Rxdata):
        self.textBrowser_2.append(str(Rxdata))
    
    def drawgraph(self):
        pen = pyqtgraph.mkPen(color=(255,0,0),width=4)
        self.data_line = self.widget.plot([i for i in range(len(deq))],list(map(float,deq)),pen=pen)
        self.widget.clear()
        deq.clear()
        self.widget.addItem(self.data_line)

class Worker(QObject):
    finished = Signal()
    progress = Signal(str)
    drawprogress = Signal()
    def __init__(self,TCPPORT,trigger):
        super().__init__(parent=None)
        self.TCPPORT = TCPPORT
        self.trigger = trigger
        self.tempdeq = tempdeq
        

    def run(self):
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        # SOCKET connection
        self.bufsize = self.sock.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)
        # self.sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        self.sock.setsockopt(socket.SOL_TCP, socket.TCP_NODELAY, 1)
        # 포트 사용 중 에러 해결
        self.sock.setsockopt(socket.SOL_SOCKET,socket.SO_SNDBUF,2048)
        self.sock.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,2048)
        self.bufsize = self.sock.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)

        self.sock.bind(self.TCPPORT)
        # Socket Bind

        self.sock.listen(5)
        # Socket Listen

        print("Waiting for incoming connections...")

        while True:
            self.conn,self.addr = self.sock.accept()
            self.conn.setblocking(True)
            self.mp = threading.Thread(target=self.receiveData,args=(self.conn,self.addr))
            self.mp.daemon = True
            self.mp.start()
    
    def receiveData(self,conn,addr):
        # 데이터 송수신
        try:
            while True:
                global deq
                data = conn.recv(self.bufsize).decode()
                if not data:
                    conn.close()
                    deq = self.tempdeq.split("\n")
                    print(deq)
                    self.tempdeq = ""
                    deq = deq[:-1]
                    self.drawprogress.emit()
                    # 데이터가 없을 때
                    break
                # Que.put(data)
                self.tempdeq+=data
                # self.progress.emit(data)
                time.sleep(self.trigger) #Trigger
                # conn.send('{}'.format(Que.get()).encode())
        except Exception as e:
            deq = self.tempdeq.split("\n")
            self.tempdeq = ""
            deq = deq[:-1]
            print("{}의 연결이 끊겼습니다.".format(addr[0]))
            conn.close()
            self.drawprogress.emit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    target=window.show()
    app.exec_()