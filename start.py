import os
import sys
import time
import threading

import numpy as np
import PIL.ImageGrab
import cv2
import win32api
import win32con
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import *

from ui_controller.view import main_window
from ui_controller.button_event import btn_events
from ui_controller.canvas_handler import canvasHandler
from utils.utils import playMGS, load_json
from corssing import crossing_detector

class main():
    def __init__(self, player):
        self.button_events = btn_events(self)
        self.win = main_window(self, self.button_events)
        self.player = player
        # self.player.play()
        self.win.show()
        self.canvasHandler = canvasHandler(self, self.win, self.win.ui.label, self.player)
        self.canvasHandler.frameSignal.connect(self.win.display_video)

        """
        初始化電子圍籬 並且將繪製好的區域加入
        下一步見 ./ui_controller/view.py 的 display_video()
        """
        self.crossing_detector = crossing_detector("A")
        ok, area = load_json('./area.txt')
        self.crossing_detector.add_area_dict(area)
        ok, area = load_json('./area2.txt')
        self.crossing_detector.add_area_dict(area)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    player = QMediaPlayer()
    MGSmp3 = './src/MGS.mp3'
    media = QUrl.fromLocalFile(MGSmp3)
    content = QMediaContent(media)
    player.setMedia(content)
    main(player)
    sys.exit(app.exec_())