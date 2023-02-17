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


def createSpinePoints(res):
    # PREPARING DATA - DICTIONARY WITH POINTS ON ALL AXIS
    points = []
    for data_point in res.pose_landmarks.landmark:
        points.append({
                        'X': data_point.x,
                        'Y': data_point.y,
                        'Z': data_point.z,
                        'Visibility': data_point.visibility})

    spineTopX1 = points[11]["X"]
    spineTopY1 = points[11]["Y"]
    spineTopZ1 = points[11]["Z"]

    spineTopX2 = points[12]["X"]
    spineTopY2 = points[12]["Y"]
    spineTopZ2 = points[12]["Z"]

    spineBotX1 = points[23]["X"]
    spineBotY1 = points[23]["Y"]
    spineBotZ1 = points[23]["Z"]

    spineBotX2 = points[24]["X"]
    spineBotY2 = points[24]["Y"]
    spineBotZ2 = points[24]["Z"]

    vec1 = np.array([spineTopX1, spineTopY1, spineTopZ1])
    vec2 = np.array([spineTopX2, spineTopY2, spineTopZ2])

    vec3 = np.array([spineBotX1, spineBotY1, spineBotZ1])
    vec4 = np.array([spineBotX2, spineBotY2, spineBotZ2])

    spineTop = (vec1 + vec2) / 2
    spineBot = (vec3 + vec4) / 2

    return spineTop, spineBot

topS, botS = createSpinePoints(res)

print(topS)