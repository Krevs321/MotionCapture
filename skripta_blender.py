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
image = cv2.imread("/Faks/Diploma/test_slika.jpg")
res = detectPose(image, pose, True)


def convert_mediapipe_landmark(landmarks, width, height):
    # Argumenti:
    # landmarks: landmarks detected from mediapipe
    # width: širina slike
    # height: dolzina slike

    #returs: list of 3D points in Blender
    
    focal_length = 500
    cx = width / 2
    cy = height / 2

    D3_points = []
    for landmark in landmarks.pose_landmarks.landmark:
        x = landmark.x * width
        y = landmark.y * height
        z = (focal_length * (cx - x)) / focal_length
        D3_points.append((x/100, y/100, z/100))

    return D3_points

converted_points = convert_mediapipe_landmark(res, image.shape[0], image.shape[1])

def createSpinePoints(points):
   
    spineTopX1 = points[11][0]
    spineTopY1 = points[11][1]
    spineTopZ1 = points[11][2]

    spineTopX2 = points[12][0]
    spineTopY2 = points[12][1]
    spineTopZ2 = points[12][2]

    spineBotX1 = points[23][0]
    spineBotY1 = points[23][1]
    spineBotZ1 = points[23][2]

    spineBotX2 = points[24][0]
    spineBotY2 = points[24][1]
    spineBotZ2 = points[24][2]

    vec1 = np.array([spineTopX1, spineTopY1, spineTopZ1])
    vec2 = np.array([spineTopX2, spineTopY2, spineTopZ2])

    vec3 = np.array([spineBotX1, spineBotY1, spineBotZ1])
    vec4 = np.array([spineBotX2, spineBotY2, spineBotZ2])

    spineTop = (vec1 + vec2) / 2
    spineBot = (vec3 + vec4) / 2

    return spineTop, spineBot

spineTop, spineBot = createSpinePoints(converted_points)

#Creating spine bone
bpy.ops.object.armature_add(enter_editmode=False, align='WORLD', location=(spineBot[0], spineBot[1], spineBot[2]), scale=(1, 1, 1))
bpy.ops.object.editmode_toggle()
bpy.ops.transform.translate(value=(spineTop[0], spineTop[1], spineTop[2]), orient_axis_ortho='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=True, use_snap_edit=True, use_snap_nonedit=True, use_snap_selectable=False)


#Extruding left arm
bpy.ops.armature.extrude_move(ARMATURE_OT_extrude={"forked":False}, TRANSFORM_OT_translate={"value":(converted_points[11][0], converted_points[11][1],converted_points[11][2]), "orient_axis_ortho":'X', "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_elements":{'INCREMENT'}, "use_snap_project":False, "snap_target":'CLOSEST', "use_snap_self":True, "use_snap_edit":True, "use_snap_nonedit":True, "use_snap_selectable":False, "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "view2d_edge_pan":False, "release_confirm":False, "use_accurate":False, "use_automerge_and_split":False})
bpy.ops.armature.extrude_move(ARMATURE_OT_extrude={"forked":False}, TRANSFORM_OT_translate={"value":(converted_points[13][0], converted_points[13][1],converted_points[13][2]), "orient_axis_ortho":'X', "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_elements":{'INCREMENT'}, "use_snap_project":False, "snap_target":'CLOSEST', "use_snap_self":True, "use_snap_edit":True, "use_snap_nonedit":True, "use_snap_selectable":False, "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "view2d_edge_pan":False, "release_confirm":False, "use_accurate":False, "use_automerge_and_split":False})
bpy.ops.armature.extrude_move(ARMATURE_OT_extrude={"forked":False}, TRANSFORM_OT_translate={"value":(converted_points[15][0], converted_points[15][1],converted_points[15][2]), "orient_axis_ortho":'X', "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_elements":{'INCREMENT'}, "use_snap_project":False, "snap_target":'CLOSEST', "use_snap_self":True, "use_snap_edit":True, "use_snap_nonedit":True, "use_snap_selectable":False, "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "view2d_edge_pan":False, "release_confirm":False, "use_accurate":False, "use_automerge_and_split":False})

bpy.data.armatures["Armature.005"].edit_bones["Bone.003"].select_tail = False
bpy.data.armatures["Armature.005"].edit_bones["Bone"].select_tail = True


#Extruding right arm
bpy.ops.armature.extrude_move(ARMATURE_OT_extrude={"forked":False}, TRANSFORM_OT_translate={"value":(converted_points[12][0], converted_points[12][1],converted_points[12][2]), "orient_axis_ortho":'X', "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_elements":{'INCREMENT'}, "use_snap_project":False, "snap_target":'CLOSEST', "use_snap_self":True, "use_snap_edit":True, "use_snap_nonedit":True, "use_snap_selectable":False, "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "view2d_edge_pan":False, "release_confirm":False, "use_accurate":False, "use_automerge_and_split":False})
bpy.ops.armature.extrude_move(ARMATURE_OT_extrude={"forked":False}, TRANSFORM_OT_translate={"value":(converted_points[14][0], converted_points[14][1],converted_points[14][2]), "orient_axis_ortho":'X', "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_elements":{'INCREMENT'}, "use_snap_project":False, "snap_target":'CLOSEST', "use_snap_self":True, "use_snap_edit":True, "use_snap_nonedit":True, "use_snap_selectable":False, "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "view2d_edge_pan":False, "release_confirm":False, "use_accurate":False, "use_automerge_and_split":False})
bpy.ops.armature.extrude_move(ARMATURE_OT_extrude={"forked":False}, TRANSFORM_OT_translate={"value":(converted_points[16][0], converted_points[16][1],converted_points[16][2]), "orient_axis_ortho":'X', "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_elements":{'INCREMENT'}, "use_snap_project":False, "snap_target":'CLOSEST', "use_snap_self":True, "use_snap_edit":True, "use_snap_nonedit":True, "use_snap_selectable":False, "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "view2d_edge_pan":False, "release_confirm":False, "use_accurate":False, "use_automerge_and_split":False})

