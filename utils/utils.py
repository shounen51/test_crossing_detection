import json

from PyQt5.QtCore import *
from PyQt5.QtMultimedia import *

def load_json(path):
    _dict={}
    try:
        with open(path,encoding="utf-8") as file:
            _dict = json.load(file)
        return True, _dict
    except:
        return False, _dict

def save_json(path, _dict):
    try:
        with open(path, "w", encoding="utf-8") as file:
            json.dump(_dict, file, indent=4, ensure_ascii=False)
        return True
    except:
        return False

def playMGS(player):
    player.play()
    print('!!')

def normalize_points(points, size1, size2=(1920,1080)):
    x_time = size2[0]/size1[0]
    y_time = size2[1]/size1[1]
    new_points = points
    for i ,(x,y) in enumerate(new_points):
        X = int(x*x_time) if int(x*x_time) < size2[0] else size2[0]
        Y = int(y*y_time) if int(y*y_time) < size2[1] else size2[1]
        new_points[i] = (X, Y)
    return new_points