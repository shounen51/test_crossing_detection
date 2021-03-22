from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import cv2
import numpy as np

from utils.utils import normalize_points
from ui.main_ui import main_form
def sort_points(points):
    x1, y1 = points[0]
    x2, y2 = points[1]
    points[0] = (min(x1,x2), min(y1,y2))
    points[1] = (max(x1,x2), max(y1,y2))
    return points
class main_window(QMainWindow):
    def __init__(self, main, event):
        QMainWindow.__init__(self)
        self.ui = main_form(self, event)
        self.main = main
        self.setWindowTitle('串流畫框')
        self.points = []

    def add_point(self, point):
        if len(self.points) == 2:
            self.points.clear()
        self.points.append(point)
        if len(self.points) == 2:
            self.points = sort_points(self.points)

    def get_draw_point(self):
        return [p for p in self.points]

    def display_video(self, args ,color = (0,255,0)):
        frame, size, label = args
        points = [p for p in self.points]
        if len(points) == 2:
            patch = frame[points[0][1]:points[1][1], points[0][0]:points[1][0],:]
            cv2.rectangle(frame, points[0], points[1], color, 2)
            for p in points:
                cv2.putText(frame, '(' + str(p[0]) + ',' + str(p[1]) + ')', p, cv2.FONT_HERSHEY_PLAIN, 2, (255,0,0), 2)
        """
        將點轉換成框並且丟到電子圍籬
        """
        self.crossing(points, size)
        width, height = size
        bytesPerComponent = 3
        bytesPerLine = bytesPerComponent * width
        qimg = QImage(frame.data, width, height, bytesPerLine, QImage.Format_RGB888)
        qimg = QPixmap.fromImage(qimg)
        label.setPixmap(qimg)

    def crossing(self, points, size):
        if len(points) == 2:
            # box必須轉換成1920*1080的大小，所以要做一次resize
            # points = normalize_points(points, size)

            # 把points轉換成xyxy格式的box
            boxes = [[points[0][0], points[0][1], points[1][0], points[1][1]]]
            boxes = np.array(boxes)
        else:
            boxes = np.array([])
        # 把box的list丟到crossing_detector的detector，回傳就會是對應的bool
        ids = self.main.crossing_detector.detector(boxes, size)
        print(ids)


