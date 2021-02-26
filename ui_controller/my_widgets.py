from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class drawable_label(QLabel):
    def __init__(self, parent, event):
        QLabel.__init__(self, parent)
        self.event = event

    def mousePressEvent(self, e):
        point = (e.pos().x(), e.pos().y())
        self.event.label_press(point)

class my_btn(QPushButton):
    def __init__(self, parent):
        QPushButton.__init__(self, parent)
        self.setStyleSheet('QPushButton {background-color: #424242; color: #E6E6E6;}')

class my_list(QListWidget):
    def __init__(self, parent):
        QListWidget.__init__(self, parent)
        self.setStyleSheet('QListWidget {background-color: #000000; color: #E6E6E6;}')

class my_edit(QTextEdit):
    def __init__(self, parent):
        QTextEdit.__init__(self, parent)
        self.setStyleSheet('QTextEdit {background-color: #000000; color: #E6E6E6;}')

class my_label(QLabel):
    def __init__(self, parent):
        QLabel.__init__(self, parent)
        self.setStyleSheet('QLabel {background-color: #000000; color: #E6E6E6;}')

class my_rdo(QRadioButton):
    def __init__(self, parent):
        QRadioButton.__init__(self, parent)
        self.setStyleSheet('QRadioButton {color: #E6E6E6;}')

class my_cb(QCheckBox):
    def __init__(self, parent):
        QCheckBox.__init__(self, parent)
        self.setStyleSheet('QCheckBox {color: #E6E6E6;}')
