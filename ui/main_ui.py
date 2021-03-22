# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Joseph\git\draw_box\ui\untitled.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from ui_controller.my_widgets import drawable_label

class main_form(QtWidgets.QWidget):
    def __init__(self, Form, event):
        QtWidgets.QWidget.__init__(self)
        Form.setObjectName("Form")
        Form.resize(1600, 900)
        Form.setMinimumSize(QtCore.QSize(1600, 900))
        Form.setMaximumSize(QtCore.QSize(1600, 900))
        self.label = drawable_label(Form, event)
        # self.label.setStyleSheet("background-image: url(./src/main.jpg);")
        self.label.setGeometry(QtCore.QRect(260, 20, 1080, 810))
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(72)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(80, 850, 91, 31))
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(24)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.rtsp_edit = QtWidgets.QLineEdit(Form)
        self.rtsp_edit.setGeometry(QtCore.QRect(180, 850, 1080, 31))
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(18)
        self.rtsp_edit.setFont(font)
        self.rtsp_edit.setPlaceholderText("")
        self.rtsp_edit.setObjectName("lineEdit")
        self.connect_rtsp_btn = QtWidgets.QPushButton(Form)
        self.connect_rtsp_btn.setGeometry(QtCore.QRect(1270, 850, 121, 31))
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(18)
        self.connect_rtsp_btn.setFont(font)
        self.connect_rtsp_btn.setObjectName("connect_rtsp_btn")

        self.save_area_btn = QtWidgets.QPushButton(Form)
        self.save_area_btn.setGeometry(QtCore.QRect(1400, 850, 121, 31))
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(18)
        self.save_area_btn.setFont(font)
        self.save_area_btn.setObjectName("save_area_btn")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
        self.event_connect(event)

    def event_connect(self, event):
        self.connect_rtsp_btn.clicked.connect(event.connect_rtsp_btn)
        self.save_area_btn.clicked.connect(event.save_area_btn)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", ""))
        self.label_2.setText(_translate("Form", "RTSP:"))
        self.connect_rtsp_btn.setText(_translate("Form", "連接"))
        self.save_area_btn.setText(_translate("Form", "儲存"))
        self.rtsp_edit.setText('rtsp://192.168.1.201:554/user=admin_password=tlJwpbo6_channel=1_stream=0.sdp?real_stream')

