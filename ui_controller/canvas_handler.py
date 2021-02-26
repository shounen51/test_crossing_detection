import cv2
import time
import numpy as np
import threading

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import *

from utils.utils import playMGS


class canvasHandler(QThread):
    frameSignal = pyqtSignal(list)
    def __init__(self, main, view, canvas, player, rtsp = ''):
        super().__init__()
        self.main = main
        self.view = view
        self.canvas = canvas
        self.player = player
        self.rtsp = rtsp
        self.size = (self.canvas.width(),self.canvas.height())
        self.retry = 5
        self.stop = True

    def start(self):
        if self.stop:
            super().start()
            self.stop = False
            print('canvasHandler start')

    def assign_rtsp(self, rtsp):
        self.rtsp = rtsp

    def get_size(self):
        return self.size

    def stop_playing(self):
        self.stop = True

    def run(self):
        self.retry = 5
        cam = cv2.VideoCapture(self.rtsp)
        if self.rtsp.startswith('rtsp://'):
            while not self.stop:
                rat, frame = cam.read()
                if rat:
                    self.retry = 5
                    frame = self.main.crossing_detector.draw_area(frame)
                    frame = cv2.resize(frame, self.size, interpolation=cv2.INTER_CUBIC)
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    self.frameSignal.emit([frame, self.size, self.canvas])
                else:
                    if self.retry > 0:
                        self.retry -= 1
                        time.sleep(0.5)
                    else:
                        sad_panda = cv2.imread('./src/sad_panda.jpg')
                        sad_panda = cv2.resize(sad_panda, self.size, interpolation=cv2.INTER_CUBIC)
                        sad_panda = cv2.cvtColor(sad_panda, cv2.COLOR_BGR2RGB)
                        self.frameSignal.emit([sad_panda, self.size, self.canvas])
                        playMGS(self.player)
                        self.stop = True
        else:
            fps = cam.get(cv2.CAP_PROP_FPS)
            rat, frame = cam.read()
            while rat:
                frame = self.main.crossing_detector.draw_area(frame)
                frame = cv2.resize(frame, self.size, interpolation=cv2.INTER_CUBIC)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                self.frameSignal.emit([frame, self.size, self.canvas])
                time.sleep(1/fps)
                rat, frame = cam.read()


