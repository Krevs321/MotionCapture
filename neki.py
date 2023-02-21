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

# Define the size of the object we'll create to represent the landmarks
LANDMARK_SIZE = 0.01

# Define a function to transform Mediapipe landmarks to 3D points
def mediapipe_to_points(mediapipe_landmarks):
    # Define the conversion matrix to convert Mediapipe coordinates to Blender coordinates
    # The matrix flips the x and y axes and scales the coordinates to match Blender's scale
    conversion_matrix = mathutils.Matrix.Scale(-1, 4, (1, 0, 0)) @ mathutils.Matrix.Scale(-1, 4, (0, 1, 0)) @ mathutils.Matrix.Scale(1, 4, (0, 0, 1)) @ mathutils.Matrix.Scale(0.1, 4)

    # Create a list to store the 3D points
    points = []

    # Loop through the landmarks and transform each one to a 3D point
    for landmark in mediapipe_landmarks:
        # Transform the landmark to a Blender-compatible point using the conversion matrix
        point = mathutils.Vector((landmark.x, landmark.y, -landmark.z, 1)) @ conversion_matrix

        # Add the point to the list of points
        points.append(point)

    # Return the list of points
    return points

# Define a function to create an object to represent a 3D point
def create_point_object(point, name):
    # Create a new mesh and object
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, mesh)

    # Set the object's location to the point's location
    obj.location = point

    # Create a new vertex at the point's location
    mesh.vertices.add(1)
    mesh.vertices[0].co = (0, 0, 0)

    # Create a new material for the object and assign it to the mesh
    mat = bpy.data.materials.new(name)
    mesh.materials.append(mat)

    # Set the material's diffuse color to white
    mat.diffuse_color = (1, 1, 1)

    # Set the object's scale to the LANDMARK_SIZE constant
    obj.scale = (LANDMARK_SIZE, LANDMARK_SIZE, LANDMARK_SIZE)

    # Return the object
    return obj

# Get the current frame of the Blender timeline
current_frame = bpy.context.scene.frame_current

# Define the Mediapipe landmarks (replace this with your own code to get the landmarks)
mediapipe_landmarks = []

image = cv2.imread("/Faks/Diploma/test_slika.jpg")
res = detectPose(image, pose, True)

for point in res.pose_landmarks.landmark:
    mediapipe_landmarks.append(point)

# Transform the Mediapipe landmarks to 3D points
points = mediapipe_to_points(mediapipe_landmarks)

# Create an object for each point and add it to the scene
for i, point in enumerate(points):
    obj = create_point_object(point, f"Landmark {i}")
    bpy.context.collection.objects.link(obj)

# Set the current frame back to its original value
bpy.context.scene.frame_set(current_frame)


# Create spine points


