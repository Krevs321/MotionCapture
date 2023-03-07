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
    image_in_RGB = cv2.flip(image_in_RGB, 1)
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


# CONVERTING MEDIAPIPE LANDMARKS TO 3D POINTS 
def mediapipePoints_3DPoints():
    results = detectPose()

    needed_points = [1, 4, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 23, 24, 25, 26, 27, 28, 31, 32]
    all_points = {}
    
    scale = 3
    z_depth = 0.2

    for i in range(len(results.pose_landmarks.landmark)):
        if i in needed_points:
            point = results.pose_landmarks.landmark[i]
            x_pose = (0.5 - point.x)*scale
            y_pose = (0.5 - point.y)*scale
            z_pose = point.z * z_depth
            all_points[i] = np.array([x_pose, y_pose, z_pose])
            #bpy.ops.mesh.primitive_cube_add(size=0.02, enter_editmode=False, align='WORLD', location=(x_pose, y_pose, z_pose), scale=(1, 1, 1))

            if i == 4:
                mid_p = middle_point(x_pose, y_pose, z_pose, results.pose_landmarks.landmark[1])
                all_points[33] = mid_p
                #bpy.ops.mesh.primitive_cube_add(size=0.02, enter_editmode=False, align='WORLD', location=(mid_p[0], mid_p[1], mid_p[2]), scale=(1, 1, 1))
            elif i == 10:
                mid_p = middle_point(x_pose, y_pose, z_pose, results.pose_landmarks.landmark[9])
                all_points[34] = mid_p
                #bpy.ops.mesh.primitive_cube_add(size=0.02, enter_editmode=False, align='WORLD', location=(mid_p[0], mid_p[1], mid_p[2]), scale=(1, 1, 1))
            elif i == 12:
                mid_p = middle_point(x_pose, y_pose, z_pose, results.pose_landmarks.landmark[11])
                all_points[35] = mid_p
                #bpy.ops.mesh.primitive_cube_add(size=0.02, enter_editmode=False, align='WORLD', location=(mid_p[0], mid_p[1], mid_p[2]), scale=(1, 1, 1))
            elif i == 20:
                mid_p = middle_point(x_pose, y_pose, z_pose, results.pose_landmarks.landmark[18])
                all_points[36] = mid_p
                #bpy.ops.mesh.primitive_cube_add(size=0.02, enter_editmode=False, align='WORLD', location=(mid_p[0], mid_p[1], mid_p[2]), scale=(1, 1, 1))
            elif i == 19:
                mid_p = middle_point(x_pose, y_pose, z_pose, results.pose_landmarks.landmark[17])
                all_points[37] = mid_p
                #bpy.ops.mesh.primitive_cube_add(size=0.02, enter_editmode=False, align='WORLD', location=(mid_p[0], mid_p[1], mid_p[2]), scale=(1, 1, 1))
            elif i == 24:
                mid_p = middle_point(x_pose, y_pose, z_pose, results.pose_landmarks.landmark[23])
                all_points[38] = mid_p 
                #bpy.ops.mesh.primitive_cube_add(size=0.02, enter_editmode=False, align='WORLD', location=(mid_p[0], mid_p[1], mid_p[2]), scale=(1, 1, 1))          
        else:
            pass
    
    return all_points

def create_bone(i, armature, list_of_points):
    if i != len(list_of_points) - 1:
        bone_name = f"Bone_{i}"
        bone = armature.edit_bones.new(bone_name)
        bone.head = list_of_points[i]
        bone.tail = list_of_points[i+1]

        return bone
    else:
        print("There is no Bone")

def select_bone(bone):
    bone.select_head = True
    bone.select_tail = True
    bone.select = True

def parent_bones(i, armature, bone, ind):
    root_bone = "Bone_0"       
    previous_bone_name = f"Bone_{i-1}" 
    if i == 0:
        previous_bone = armature.edit_bones.get(root_bone)    
    else:
        previous_bone = armature.edit_bones.get(previous_bone_name)
    select_bone(bone)
    select_bone(previous_bone)
    armature.edit_bones.active = previous_bone
    
    if (ind == 2 or ind == 3):    
        bpy.ops.armature.parent_set(type='OFFSET')
        bpy.ops.armature.select_all(action='DESELECT') 
    else:  
        bpy.ops.armature.parent_set(type='CONNECTED')
        bpy.ops.armature.select_all(action='DESELECT')

def parent_limbs(i, armature, bone):       
    previous_bone_name = f"Bone_limb_{i}" 
    previous_bone = armature.edit_bones.get(previous_bone_name)
    select_bone(bone)
    select_bone(previous_bone)
    armature.edit_bones.active = previous_bone
    bpy.ops.armature.parent_set(type='CONNECTED')
    bpy.ops.armature.select_all(action='DESELECT')

def create_armature():
    points = mediapipePoints_3DPoints()

    armature = bpy.data.armatures.new('Armature')
    object = bpy.data.objects.new('Armature', armature)
    bpy.context.scene.collection.objects.link(object)
    bpy.context.view_layer.objects.active = object
    bpy.ops.object.mode_set(mode='EDIT')

    main_bones = [points[38], points[35], points[34], points[33]]
    
    left_arm_st = [points[35], points[11]]
    left_arm = [points[11], points[13], points[15], points[37]]
    
    right_arm_st = [points[35], points[12]]
    right_arm = [points[12], points[14], points[16], points[36]]
    
    left_leg_st = [points[24], points[26]]
    left_leg = [points[26], points[28], points[32]]
    
    right_leg_st = [points[23], points[25]]
    right_leg = [points[25], points[27], points[31]]
    
    limbs_start = [left_arm_st, right_arm_st, left_leg_st, right_leg_st]
    limbs_other = [left_arm, right_arm, left_leg, right_leg]   
    
    for i in range(len(main_bones)):
        main_bone = create_bone(i, armature, main_bones)
        if i > 0: 
            if i != len(main_bones) - 1:
                parent_bones(i, armature, main_bone, 5)
            else:
                pass     
    
    for i in range(len(limbs_start)):
        limb_bone_name = f"Bone_limb_{i}"
        bone = armature.edit_bones.new(limb_bone_name)
        bone.head = limbs_start[i][0]
        bone.tail = limbs_start[i][1]
        if i == 2 or i == 3:
            parent_bones(0, armature, bone, i)
        else:
            parent_bones(0, armature, bone, 5)
    
    for i in range(len(limbs_other)):
        for j in range(len(limbs_other[i])):     
            limb = create_bone(j, armature, limbs_other[i])
            
            
    
    
#    right_arm_bone_name = "Bone_right_arm_0"
#    bone = armature.edit_bones.new(right_arm_bone_name)
#    bone.head = right_arm_st[0]
#    bone.tail = right_arm_st[1]
#    parent_bones(0, armature, bone, 5)
#    
#    
#    left_leg_bone_name = "Bone_left_leg_0"
#    bone = armature.edit_bones.new(left_leg_bone_name)
#    bone.head = left_leg_st[0]
#    bone.tail = left_leg_st[1]
#    parent_bones(0, armature, bone, 2)
#    
#    right_leg_bone_name = "Bone_right_leg_0"
#    bone = armature.edit_bones.new(right_arm_bone_name)
#    bone.head = right_leg_st[0]
#    bone.tail = right_leg_st[1]
#    parent_bones(0, armature, bone, 3)
               
    # create_bone(armature, right_arm)
    # create_bone(armature, left_leg)
    # create_bone(armature, right_leg)
        

        
#        root_bone = "Bone_0"
#        previous_bone = ""
#        if i > 0:
#            if (i == 3 and i+1 == 4) or (i == 8 and i+1 == 9):
#                previous_bone = armature.edit_bones.get(root_bone)
#            else:
#                previous_bone_name = f"Bone_{i-1}"
#                previous_bone = armature.edit_bones.get(previous_bone_name)
#            select_bone(bone)
#            select_bone(previous_bone)
#            armature.edit_bones.active = previous_bone
#            
#            bpy.ops.armature.parent_set(type='CONNECTED')
#            bpy.ops.armature.select_all(action='DESELECT')
            
 

    return points

create_armature()