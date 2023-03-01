

import mediapipe as mp
import cv2
import numpy as np
import bpy
import mathutils


def detectPose():
    mp_pose = mp.solutions.pose
    image = cv2.imread("/Faks/Diploma/test_slika.jpg")
    # pose_image = mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.5)
    pose = mp_pose.Pose()
    image_in_RGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    resultant = pose.process(image_in_RGB)
            
    return resultant


# Results from mediapipe
results = detectPose()

# Metoda ki izračuna sredinsko točko med medenico in ključnico (zgornji del hrbtenice in spodnji del hrbtenice). 
# Args: x,y,z trenutne točke
# Return: sredinska točka na podlagi trenutne in naslednje točke
def middle_point(x_c, y_c, z_c, p_next):
    scale = 2
    z_depth = 0

    x_next = (0.5-p_next.x)*scale
    y_next = (0.5-p_next.y)*scale
    z_next = p_next.z*z_depth

    vec1 = np.array([x_c, y_c, z_c])
    vec2 = np.array([x_next, y_next, z_next])
    
    mid_point = (vec1 + vec2) / 2

    return mid_point

# CONVERTING MEDIAPIPE LANDMARKS TO 3D POINTS 
def mediapipePoints_3DPoints():
    scale = 2
    z_depth = 0.2

    converted_points = []
    needed_points = [11, 12, 13, 14, 15, 16, 23, 24, 25, 26, 27, 28, 31, 32, 0]

    for i in range(len(results.pose_landmarks.landmark)):
        if i in needed_points:
            x_pose = (0.5-results.pose_landmarks.landmark[i].x)*scale
            y_pose = (0.5-results.pose_landmarks.landmark[i].y)*scale
            z_pose = results.pose_landmarks.landmark[i].z*z_depth
            
            if (i == 11 and i+1 == 12):
                next_point = results.pose_landmarks.landmark[i+1]
                p = middle_point(x_pose, y_pose, z_pose, next_point)
                converted_points.append(p)
                bpy.ops.mesh.primitive_cube_add(size=0.05, enter_editmode=False, align='WORLD', location=(p[0], p[1], p[2]), scale=(1, 1, 1))

            elif (i == 23 and i+1 == 24):
                next_point = results.pose_landmarks.landmark[i+1]
                p = middle_point(x_pose, y_pose, z_pose, next_point)
                converted_points.append(p)
                bpy.ops.mesh.primitive_cube_add(size=0.05, enter_editmode=False, align='WORLD', location=(p[0], p[1], p[2]), scale=(1, 1, 1))

            elif i == 12 or i == 24:
                converted_points.append(np.array([x_pose, y_pose, z_pose]))
            else:
                converted_points.append(np.array([x_pose, y_pose, z_pose])) 
        else:
            pass
        
        bpy.ops.mesh.primitive_cube_add(size=0.05, enter_editmode=False, align='WORLD', location=(x_pose, y_pose, z_pose), scale=(1, 1, 1))

    return converted_points



def create_armature():
    points = mediapipePoints_3DPoints()
    armature = bpy.data.armatures.new('Armature')
    object = bpy.data.objects.new('Armature', armature)
    bpy.context.scene.collection.objects.link(object)
    bpy.context.view_layer.objects.active = object
    bpy.ops.object.mode_set(mode='EDIT')

    # Spine to neck bones
    # main_bones = [points[0], points[7], points[1]]
   
    bone_name = "Bone_1"
    bone = armature.edit_bones.new(bone_name)
    bone.head = points[7]
    bone.tail = points[1]
    bone_name = "Bone_2"
    bone = armature.edit_bones.new(bone_name)
    bone.head = points[1]
    bone.tail = points[0]
    
    bpy.data.armatures["Aarmature"].edit_bones.get["Bone_1"]

    # update the armature
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.mode_set(mode='EDIT')
    armature.update()
    bpy.ops.object.mode_set(mode='EDIT')

p = create_armature()
