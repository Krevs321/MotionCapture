

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
    results = detectPose()

    scale = 2
    z_depth = 0.2

    converted_points = []
    needed_points = [11, 12, 13, 14, 15, 16, 23, 24, 25, 26, 27, 28, 31, 32, 0]

    for i in range(len(results.pose_landmarks.landmark)):
        if i in needed_points:
            x_pose = (0.5 - results.pose_landmarks.landmark[i].x)*scale
            y_pose = (0.5 - results.pose_landmarks.landmark[i].y)*scale
            z_pose = results.pose_landmarks.landmark[i].z*z_depth
            if (i == 11 and i+1 == 12):
                converted_points.append(np.array([x_pose, y_pose, z_pose]))
                next_point = results.pose_landmarks.landmark[i+1]
                p = middle_point(x_pose, y_pose, z_pose, next_point)
                converted_points.append(p)
            elif (i == 23 and i+1 == 24):
                converted_points.append(np.array([x_pose, y_pose, z_pose]))
                next_point = results.pose_landmarks.landmark[i+1]
                p = middle_point(x_pose, y_pose, z_pose, next_point)
                converted_points.append(p)
            elif i == 12 or i == 24:
                converted_points.append(np.array([x_pose, y_pose, z_pose]))
            else:
                converted_points.append(np.array([x_pose, y_pose, z_pose])) 
        else:
            pass
        
    return converted_points



def create_armature():
    points = mediapipePoints_3DPoints()
    armature = bpy.data.armatures.new('Armature')
    object = bpy.data.objects.new('Armature', armature)
    bpy.context.scene.collection.objects.link(object)
    bpy.context.view_layer.objects.active = object
    bpy.ops.object.mode_set(mode='EDIT')

    # Spine to neck bones
    new_points = [points[9], points[2], points[0], 
                    points[2], points[1], points[4], points[6], 
                    points[2], points[3], points[5], points[7], 
                    points[9], points[8], points[11], points[13], points[15],
                    points[9], points[10], points[12], points[14], points[16]]
     
   
    for i in range(len(new_points)):
        if i == 2 or i == 6 or i == 10 or i == 15 or i == 20:
            pass
        else:
        
            bone_name = f"Bone_{i}"
            bone = armature.edit_bones.new(bone_name)
            bone.head = new_points[i]
            bone.tail = new_points[i+1]
            #bpy.ops.armature.extrude_move(ARMATURE_OT_extrude={"forked":False}, TRANSFORM_OT_translate={"value": new_points[i], "orient_axis_ortho":'X', "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_elements":{'INCREMENT'}, "use_snap_project":False, "snap_target":'CLOSEST', "use_snap_self":False, "use_snap_edit":False, "use_snap_nonedit":False, "use_snap_selectable":False, "snap_point":new_points[i], "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "view2d_edge_pan":False, "release_confirm":False, "use_accurate":False, "use_automerge_and_split":False})


    return points

p = create_armature()
