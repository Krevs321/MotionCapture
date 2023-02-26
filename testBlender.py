import subprocess
import sys
import os

# path to python.exe
python_exe = os.path.join(sys.prefix, 'bin', 'python.exe')
py_lib = os.path.join(sys.prefix, 'lib', 'site-packages','pip')

# install opencv
subprocess.call([python_exe, py_lib, "install", "opencv_python"])
# install mediapipe
subprocess.call([python_exe, py_lib, "install", "mediapipe"])


import mediapipe as mp
import cv2
import numpy as np
import bpy
from mathutils import Vector


# PREPARING DATA FOR DETECTING A POSE IN IMAGE
mp_pose = mp.solutions.pose
pose_image = mp_pose.Pose(static_image_mode=True, 
                          min_detection_confidence=0.5)
pose_video = mp_pose.Pose(static_image_mode=False, 
                          min_detection_confidence=0.7,
                          min_tracking_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils
pose = mp_pose.Pose()

def detectPose(image_pose, pose, draw=False):
    image_in_RGB = cv2.cvtColor(image_pose, cv2.COLOR_BGR2RGB)
    resultant = pose.process(image_in_RGB)
            
    return resultant


# PREPARING IMAGE
D = bpy.data
image = cv2.imread("/Faks/Diploma/test_slika.jpg")
res = detectPose(image, pose, True)

points = []
for point in res.pose_landmarks.landmark:
    points.append((point.x, point.y))

