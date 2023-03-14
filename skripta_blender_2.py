
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
                mid_point = middle_point(x_pose, y_pose, z_pose, results.pose_landmarks.landmark[i+1])
                converted_points.append(mid_point)
                #bpy.ops.mesh.primitive_cube_add(size=0.02, enter_editmode=False, align='WORLD', location=(mid_point[0], mid_point[1], mid_point[2]), scale=(1, 1, 1))

            elif (i == 23 and i+1 == 24):# CALCULATE BOT OF THE SPINE
                converted_points.append(np.array([x_pose, y_pose, z_pose]))
                mid_point = middle_point(x_pose, y_pose, z_pose, results.pose_landmarks.landmark[i+1])
                converted_points.append(mid_point)
                #bpy.ops.mesh.primitive_cube_add(size=0.02, enter_editmode=False, align='WORLD', location=(mid_point[0], mid_point[1], mid_point[2]), scale=(1, 1, 1))

            elif (i == 18 and i+2 == 20): # CALCULATE MIDDLE POINT OF HAND
                next_point = results.pose_landmarks.landmark[i+2]
                mid_point = middle_point(x_pose, y_pose, z_pose, next_point)
                converted_points.append(mid_point)
                #bpy.ops.mesh.primitive_cube_add(size=0.02, enter_editmode=False, align='WORLD', location=(mid_point[0], mid_point[1], mid_point[2]), scale=(1, 1, 1))

            elif (i == 17 and i+2 == 19): # CALCULATE MIDDLE POINT OF HAND
                next_point = results.pose_landmarks.landmark[i+2]
                mid_point = middle_point(x_pose, y_pose, z_pose, next_point)
                converted_points.append(mid_point)
                #bpy.ops.mesh.primitive_cube_add(size=0.02, enter_editmode=False, align='WORLD', location=(mid_point[0], mid_point[1], mid_point[2]), scale=(1, 1, 1))
           
            elif i == 12 or i == 24:
                converted_points.append(np.array([x_pose, y_pose, z_pose]))
            
            else:
                converted_points.append(np.array([x_pose, y_pose, z_pose])) 
            
            #bpy.ops.mesh.primitive_cube_add(size=0.02, enter_editmode=False, align='WORLD', location=(x_pose, y_pose, z_pose), scale=(1, 1, 1))

        else:
            pass
        
    return converted_points

def select_bone(bone):
    bone.select_head = True
    bone.select_tail = True
    bone.select = True

def create_bone(i, armature, new_points):
    if i == len(new_points)-1 or i == 2:
        pass
    else:
        bone_name = f"Bone_{i}"
        bone = armature.edit_bones.new(bone_name)
        bone.head = new_points[i]
        bone.tail = new_points[i+1]
        
        parent_bones(i, bone, armature)
        
    root_bone_name = "Bone_0"
    root_bone = armature.edit_bones.get(root_bone_name)
    select_bone(root_bone)
                    

def parent_bones(i, bone, armature):
    previous_bone_name = f"Bone_{i-1}"
    if i > 0:      
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

    # ALL 3D POINTS NEEDED TO CREATE ARMATURE
#    new_points = [points[13], points[2], points[0],
#                    points[2], points[1], points[4], points[6], points[8],
#                    points[2], points[3], points[5], points[7], points[9],
#                    points[13], points[12], points[15], points[17], points[19],
#                    points[14], points[16], points[18], points[20]]
                  
    main_bones_names = ["Bone1", "Bone2", "Bone3"]             
    main_bones =  [points[13], points[2], points[0]]
    left_arm  = [points[2], points[1], points[4], points[6], points[8]] 
#    right_arm = [points[2], points[3], points[5], points[7], points[9]] 
#    right_leg = [points[12], points[15], points[17], points[19]] 
#    left_leg = [points[14], points[16], points[18], points[20]]    
#    
#    for i in range(len(main_bones)):
#        bone = create_bone(i, armature, main_bones)
    for i in range(len(main_bones)):
        bone = create_bone(i, armature, main_bones)
         
    for i in range(len(left_arm)):
        bone_name = f"Bone_left_{i}"
        bone = armature.edit_bones.new(bone_name)
        bone.head = left_arm[i]
        bone.tail = left_arm[i+1]
    
        
    
#    for i in range(len(right_arm)):
#        bone = create_bone(i, armature, right_arm)
#    for i in range(len(left_leg)):
#        bone = create_bone(i, armature, right_leg)

#    for i in range(len(right_leg)):
#        bone = create_bone(i, armature, left_leg)

        
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