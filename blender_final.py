import bpy
import sys
import os
import pathlib
import importlib

sys.path.append("c:\\Users\\Gasper Krevs\\AppData\\Local\\Programs\\Python\\Python310\\lib\\site-packages\\cv2\\")
sys.path.append("d:\\Faks\\Diploma\\functions.py")

import cv2
from functions import *

image = cv2.imread("test_slika.jpg")
slika, lndmrks = detectPose(image, pose, True)
spineTop, spineBot = createSpinePoints(lndmrks)
