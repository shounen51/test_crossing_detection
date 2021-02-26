import time
import datetime
import sys
import json

import cv2
import numpy as np

def _check_timeSlot(timeSlot):
    now24H = int(time.strftime("%H", time.localtime()))
    if timeSlot[0] > timeSlot[1]:
        if now24H > timeSlot[0] or now24H < timeSlot[1]:
            return True
        else:
            return False
    else:
        if now24H > timeSlot[0] and now24H < timeSlot[1]:
            return True
        else:
            return False

def _check_week(week):
    now = datetime.date.today().weekday()
    if week[now] == '1':
        return True
    else:
        return False

class area():
    def __init__(self, areaDict):
        self.type = areaDict['alertType']
        self.ab = areaDict['area']['abs']
        self.points = areaDict['area']['points']
        self.week = areaDict['day']
        _t = areaDict['hour'].split(',')
        self.areaName = areaDict['areaName']
        self.timeSlot = (int(_t[0]),int(_t[1]))
        sec = float(areaDict['sec'])
        if sec > 0.1:
            self.residenceTimeLimit = float(areaDict['sec'])
        else:
            self.residenceTimeLimit = 0.1
        self.residenceTime = 0
        self.lastTimmer = time.time()
        self.stopTimmer = 0
        self.timeMode = 0 # 0=down 1=raise 2=stop

    def trigger(self):
        if self.timeMode != 1:
            self.timeMode = 1
            addTime = 0
        else:
            addTime = time.time() - self.lastTimmer
        if self.residenceTime + addTime < self.residenceTimeLimit:
            self.residenceTime += addTime
        else:
            self.residenceTime = self.residenceTimeLimit
        self.lastTimmer = time.time()
        alarm = False
        if self.residenceTime == self.residenceTimeLimit:
            alarm = True
            # self.residenceTime = 0
        return alarm

    def safe(self):
        if self.timeMode == 1:
            self.timeMode = 2
            self.stopTimmer = time.time()
        elif self.timeMode == 2:
            stopTime = time.time() - self.stopTimmer
            if stopTime > 1:
                self.timeMode = 0
        else:
            if self.residenceTime > 0:
                addtime = time.time() - self.lastTimmer
                if self.residenceTime - addtime > 0:
                    self.residenceTime -= addtime
                else:
                    self.residenceTime = 0
        self.lastTimmer = time.time()

    def get_color(self):
        if not _check_timeSlot(self.timeSlot):
            return (120,120,120)
        elif not _check_week(self.week):
            return (120,120,120)
        else:
            H = int((1-(self.residenceTime/self.residenceTimeLimit))*60)
            S = 255
            V = 255
            a = np.array([[[H,S,V]]],dtype='uint8')
            a = cv2.cvtColor(a, cv2.COLOR_HSV2BGR)
            B,G,R = int(a[0,0,0]),int(a[0,0,1]),int(a[0,0,2])
            return (B,G,R)


class crossing_detector():
    def __init__(self):
        self.areaDict = {}

    def get_area_dict(self):
        return self.areaDict

    def add_area(self, _dict):
        _area = area(_dict)
        if _dict["areaName"] == "": _dict["areaName"] = str(len(self.areaDict))
        self.areaDict[_dict["areaName"]] = _area

    def del_area(self, name):
        self.areaDict.pop(name, None)

    def _bbox2cxdyty(self, bbox_xyxy):
        cxdyty = np.empty((bbox_xyxy.shape[0],3))
        cxdyty[:,0] = (bbox_xyxy[:,0] + bbox_xyxy[:,2])/2
        cxdyty[:,1] = bbox_xyxy[:,3]
        cxdyty[:,2] = bbox_xyxy[:,1]
        return cxdyty



    def detector(self, bbox_xyxy):
        trackThem = np.zeros([], dtype=bool)
        if len(bbox_xyxy) == 0:
            for aindex, areaName in enumerate(self.areaDict):
                area = self.areaDict[areaName]
                area.safe()
            return []
        bboxes = self._bbox2cxdyty(bbox_xyxy)
        temp = np.zeros([bboxes.shape[0],len(self.areaDict)], dtype=bool)
        trackThem = np.zeros([bboxes.shape[0],len(self.areaDict)], dtype=bool)
        alarmType = '0'
        for aindex, areaName in enumerate(self.areaDict):
            area = self.areaDict[areaName]
            if not _check_timeSlot(area.timeSlot):
                continue
            if not _check_week(area.week):
                continue
            td = 1
            temp = is_point_in_here(temp, aindex, area, bboxes, td)
            alarm = False
            if temp[:,aindex].any() == True:
                if area.type == 1:
                    td = 2
                    temp2 = np.zeros([bboxes.shape[0],len(self.areaDict)], dtype=bool)
                    temp2 = is_point_in_here(temp2, aindex, area, bboxes, td)
                    temp2[:,aindex] = np.logical_not(temp2[:,aindex])
                    temp[:,aindex] = np.logical_and(temp[:,aindex], temp2[:,aindex])
                    if temp[:,aindex].any() == True:
                        alarm = area.trigger()
                else:
                    alarm = area.trigger()
            else:
                area.safe()
            if alarm:
                trackThem[:,aindex] = temp[:,aindex]
                alarmType = area.type
        return trackThem

    def draw_area(self, img):
        for areaName in self.areaDict:
            area = self.areaDict[areaName]
            for index, point in enumerate(area.points):
                index -= len(area.points)
                p1 = (point[0], point[1])
                p2 = (area.points[index+1][0], area.points[index+1][1])
                cv2.line(img, p1, p2, area.get_color(),3)
        return img

def is_point_in_here(temp, aindex, area, bboxes, td):
    for index,(a, b) in enumerate(area.ab):
        index -= len(area.ab)
        ytemp = a*bboxes[:,0] + b
        point1, point2 = area.points[index], area.points[index+1]

        left = np.full_like(ytemp, min(point1[0], point2[0]))
        right = np.full_like(ytemp, max(point1[0], point2[0]))
        top = np.full_like(ytemp, min(point1[1], point2[1]))
        bottom = np.full_like(ytemp, max(point1[1], point2[1]))

        _mask = ytemp >= bboxes[:,td]
        _mask2 = np.logical_and(top <= ytemp, ytemp <= bottom)
        _mask3 = np.logical_and(left <= bboxes[:,0], bboxes[:,0] <= right)

        _mask = np.logical_and(_mask, _mask2)
        _mask = np.logical_and(_mask, _mask3)
        temp[:,aindex] = np.logical_xor(temp[:,aindex], _mask)
    return temp

if __name__ == "__main__":
    areaSetList=[{
        'area' : {"abs": [[0.009, 756.872], [3.08, -3634.4], [0.001, 1076.47], [-3.33, 3401.34]], "points": [[792, 764], [1430, 770], [1530, 1078], [698, 1077]]},
        'alertType' : '0',
        'areaName':'test',
        'day':'1111111',
        'hour':'0,24',
        'sec':'2',
        'cam':'52'
    }]
    detector = crossing_detector()
    bbox_xyxy_list = [np.array([[932,970,1230,971]])]
    while 1:
        returnList = detector.detector([0],bbox_xyxy_list)
        print(returnList)
        print('--------------------')
        time.sleep(0.5)
