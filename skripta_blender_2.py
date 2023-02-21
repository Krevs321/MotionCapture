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
import mathutils


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
image = cv2.imread("/Faks/Diploma/test_slika.jpg")
res = detectPose(image, pose, True)

# CONVERTING MEDIAPIPE LANDMARKS TO 3D POINTS 
# Function returns: list of transformed points

def mediapipe_to_points(landmarks):
    # Define the conversion matrix to convert Mediapipe coordinates to Blender coordinates
    # The matrix flips the x and y axes and scales the coordinates to match Blender's scale
    conversion_matrix = mathutils.Matrix.Scale(-1, 4, (1, 0, 0)) @ mathutils.Matrix.Scale(-1, 4, (0, 1, 0)) @ mathutils.Matrix.Scale(1, 4, (0, 0, 1)) @ mathutils.Matrix.Scale(0.1, 4)

    # Create a list to store the 3D points
    points = []

    # Loop through the landmarks and transform each one to a 3D point
    for landmark in landmarks.pose_landmarks.landmark:
        # Transform the landmark to a Blender-compatible point using the conversion matrix
        point = mathutils.Vector((landmark.x, landmark.y, -landmark.z)) @ conversion_matrix

        # Add the point to the list of points
        points.append(point)

    # Return the list of points
    return points
    

converted_points = mediapipe_to_points(res)

print(converted_points)