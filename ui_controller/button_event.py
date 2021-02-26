import time
import json

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from utils.utils import normalize_points, save_json
class btn_events():
    def __init__(self, main):
        self.main = main

    def label_press(self, point):
        self.main.win.add_point(point)

    def connect_rtsp_btn(self):
        self.main.canvasHandler.stop_playing()
        time.sleep(0.1)
        rtsp = self.main.win.ui.rtsp_edit.text()
        self.main.canvasHandler.assign_rtsp(rtsp)
        self.main.canvasHandler.start()

    def save_area_btn(self):
        _area_dict = {'cam': 'cam0', 'areaName': '', 'area': {"abs": [], "points": []}, 'alertType': '1', 'day': '1111111', 'hour': '0,24', 'sec': '0'}
        _name = "123"
        _H_start = '0'
        _H_end = '24'
        _sec = '1'
        _points = self.main.win.get_draw_point()
        _weekday = '1111111'
        _abs = []
        _1080points = normalize_points([p for p in _points], self.main.canvasHandler.get_size(), size2=(1920,1080))
        _1080points.append(_1080points[0])
        for i in range(len(_1080points)-1):
            x1,y1 = _1080points[i]
            x2,y2 = _1080points[i+1]
            if x1-x2 == 0:
                a = float('inf')
                b = 0
            else:
                a = round((y1-y2)/(x1-x2),3)
                b = round(y1 - x1*a,3)
            _abs.append((a,b))
        _1080points.pop()
        _area = {'abs': _abs, 'points': _1080points}
        _area_dict['area'] = _area
        save_json('./area.txt', _area_dict)
        self.main.crossing_detector.add_area(_area_dict)
        self.main.win.add_point(_points[0])