

import mediapipe as mp
import cv2
import numpy as np
import bpy
import mathutils


def detectPose():
    mp_pose = mp.solutions.pose
    image = cv2.imread("/Faks/Diploma/test_slika2.jpg")
    # pose_image = mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.5)
    pose = mp_pose.Pose()
    image_in_RGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    resultant = pose.process(image_in_RGB)
            
    return resultant


# Metoda ki izračuna sredinsko točko med medenico in ključnico (zgornji del hrbtenice in spodnji del hrbtenice). 
# Args: x,y,z trenutne točke
# Return: sredinska točka na podlagi trenutne in naslednje točke
def middle_point(x_c, y_c, z_c, p_next):
    scale = 3
    z_depth = 0.2
    
    x_next = (0.5-p_next.x)*scale
    y_next = (0.5-p_next.y)*scale
    z_next = p_next.z*z_depth

    vec1 = np.array([x_c, y_c, z_c])
    vec2 = np.array([x_next, y_next, z_next])
    
    mid_point = (vec1 + vec2) / 2

    return mid_point

def calculate_coordinates(point):
    scale = 3
    z_depth = 0.2
    
    x_pose = (0.5 - point.x)*scale
    y_pose = (0.5 - point.y)*scale
    z_pose = point.z * z_depth

    return x_pose, y_pose, z_pose

# CONVERTING MEDIAPIPE LANDMARKS TO 3D POINTS 
def mediapipePoints_3DPoints():
    results = detectPose()

    converted_points = []
    needed_points = [11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 23, 24, 25, 26, 27, 28, 31, 32, 0]

    for i in range(len(results.pose_landmarks.landmark)):
        if i in needed_points:
            point = results.pose_landmarks.landmark[i]
            x_pose, y_pose, z_pose = calculate_coordinates(point)
            
            if (i == 11 and i+1 == 12): # CALCULATE TOP OF THE SPINE
                converted_points.append(np.array([x_pose, y_pose, z_pose]))
                next_point = results.pose_landmarks.landmark[i+1]
                mid_point = middle_point(x_pose, y_pose, z_pose, next_point)
                converted_points.append(mid_point)
            elif (i == 23 and i+1 == 24):# CALCULATE BOT OF THE SPINE
                converted_points.append(np.array([x_pose, y_pose, z_pose]))
                next_point = results.pose_landmarks.landmark[i+1]
                mid_point = middle_point(x_pose, y_pose, z_pose, next_point)
                converted_points.append(mid_point)
            elif (i == 18 and i+2 == 20): # CALCULATE MIDDLE POINT OF HAND
                next_point = results.pose_landmarks.landmark[i+2]
                mid_point = middle_point(x_pose, y_pose, z_pose, next_point)
                converted_points.append(mid_point)
            elif (i == 17 and i+2 == 19): # CALCULATE MIDDLE POINT OF HAND
                next_point = results.pose_landmarks.landmark[i+2]
                mid_point = middle_point(x_pose, y_pose, z_pose, next_point)
                converted_points.append(mid_point)           
            elif i == 12 or i == 24:
                converted_points.append(np.array([x_pose, y_pose, z_pose]))
            else:
                converted_points.append(np.array([x_pose, y_pose, z_pose])) 
            
        else:
            pass
        
    return converted_points

def select_bone(bone):
    #bone.select_head = True
    #bone.select_tail = True
    bone.select = True

def create_bone(i, armature, new_points):
    if i == 2 or i == 7 or i == 12 or i == 17 or i == 21 or i == 13:
        pass
    else:
        bone_name = f"Bone_{i}"
        bone = armature.edit_bones.new(bone_name)
        bone.head = new_points[i]
        bone.tail = new_points[i+1]
        
        return bone
    
def create_armature():
    points = mediapipePoints_3DPoints()
    armature = bpy.data.armatures.new('Armature')
    object = bpy.data.objects.new('Armature', armature)
    bpy.context.scene.collection.objects.link(object)
    bpy.context.view_layer.objects.active = object
    bpy.ops.object.mode_set(mode='EDIT')

    # ALL 3D POINTS NEEDED TO CREATE ARMATURE
    new_points = [points[13], points[2], points[0],
                    points[2], points[1], points[4], points[6], points[8],
                    points[2], points[3], points[5], points[7], points[9],
                    points[13], points[12], points[15], points[17], points[19],
                    points[14], points[16], points[18], points[20]]
    
    for i in range(len(new_points)):
        bone = create_bone(i, armature, new_points)

        root_bone = "Bone_0"
        previous_bone = ""
        if i > 0:
            if (i == 3 and i+1 == 4) or (i == 8 and i+1 == 9):
                previous_bone = armature.edit_bones.get(root_bone)
            else:
                previous_bone_name = f"Bone_{i-1}"
                previous_bone = armature.edit_bones.get(previous_bone_name)
            select_bone(bone)
            select_bone(previous_bone)
            armature.edit_bones.active = previous_bone
            
            bpy.ops.armature.parent_set(type='CONNECTED')
            bpy.ops.armature.select_all(action='DESELECT')
            
        root = "Bone_0"
        test_b = armature.edit_bones.get(root)
        test_b.select_head = True

    return points

create_armature()