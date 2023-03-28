import mediapipe as mp
import cv2
import numpy as np
import bpy
import mathutils


def detectPose(image):
    mp_pose = mp.solutions.pose
    #image = cv2.imread("/Faks/Diploma/test_slika2.jpg")
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
def mediapipePoints_3DPoints(results):
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

def create_bone(i, armature, list_of_points, bone_names):
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


def create_armature(points):

    armature = bpy.data.armatures.new('Armature')
    object = bpy.data.objects.new('Armature', armature)
    bpy.context.scene.collection.objects.link(object)
    bpy.context.view_layer.objects.active = object
    bpy.ops.object.mode_set(mode='EDIT')

    main_bones = [points[38], points[35], points[34], points[33]]
    
    left_arm = [points[11], points[13], points[15], points[37]]    
    right_arm = [points[12], points[14], points[16], points[36]]    
    left_leg = [points[24], points[26], points[28], points[32]]   
    right_leg = [points[23], points[25], points[27], points[31]]
 
    limbs_other = [left_arm, right_arm, left_leg, right_leg] 
    limbs_other_names = ["left_arm", "right_arm", "left_leg", "right_leg"]     
    
    for i in range(len(main_bones)):
        main_bone = create_bone(i, armature, main_bones, None)
        if i > 0: 
            if i != len(main_bones) - 1:
                parent_bones(i, armature, main_bone, 5)
            else:
                pass     
    
    for i in range(len(limbs_other)):
        previous = limbs_other[i][0]
        for j in range(len(limbs_other[i])):     
            limb = create_bone(j, armature, limbs_other[i], limbs_other_names)
            if j == 0 :
                parent_bones(j, armature, limb, 2)
                previous = limb
            else:
                if j < len(limbs_other[i]) - 1:
                    select_bone(limb)
                    select_bone(previous)
                    armature.edit_bones.active = previous
                    bpy.ops.armature.parent_set(type='CONNECTED')
                    bpy.ops.armature.select_all(action='DESELECT') 
                    previous = limb
                else:
                    print("Done!") 
    
    bpy.ops.object.mode_set(mode='OBJECT')
    return points
                

def read_video(image_path):
    cam = cv2.VideoCapture(image_path)
      
    currentframe = 0
    while(True):
        ret,frame = cam.read()
          
        if ret:
            print(f"Creating frame: {currentframe}")
        
            results = detectPose(frame)
            points = mediapipePoints_3DPoints(results)
            create_armature(points)
            currentframe += 1
        else:
            break
    print(currentframe)
    cam.release()
    cv2.destroyAllWindows()
    return currentframe
        
def read_image(image_path):
    print(f"Creating frame: 0")
    
    frame = cv2.imread(image_path)
    results = detectPose(frame)
    points = mediapipePoints_3DPoints(results)
    create_armature(points)
       

video_path = "/Faks/Diploma/test_video.mp4"
frames = read_video(video_path)

image_path = "/Faks/Diploma/test_slika3.jpg"
#read_image(image_path)

image_path = "/Faks/Diploma/test_slika2.jpg"
#read_image(image_path)

source_armature = bpy.data.objects['Armature']
frames = 71

bpy.context.view_layer.objects.active = source_armature
source_armature.select_set(True)
bpy.ops.object.mode_set(mode='POSE')
bpy.ops.pose.select_all(action='SELECT')
bpy.ops.anim.keyframe_insert_by_name(type="BUILTIN_KSI_LocScale")

for i in range(1, frames):
    bpy.context.scene.frame_end = frames

    target_armature_name = f"Armature.{i :03}"
    target_armature = bpy.data.objects[target_armature_name]

    bpy.context.view_layer.objects.active = target_armature

    bpy.data.scenes['Scene'].frame_set(bpy.data.scenes['Scene'].frame_current + 1)
    #bpy.data.scenes['Scene'].frame_set(bpy.data.scenes['Scene'].frame_end)

    for bone in target_armature.pose.bones:
        source_armature.pose.bones[bone.name].matrix = bone.matrix
        source_armature.pose.bones[bone.name].scale = bone.scale

    bpy.ops.pose.select_all(action='SELECT')
    bpy.ops.anim.keyframe_insert_by_name(type="BUILTIN_KSI_LocScale")


bpy.ops.object.posemode_toggle()
