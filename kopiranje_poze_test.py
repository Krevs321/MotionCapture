import bpy


source_armature = bpy.data.objects['Armature']
target_armature = bpy.data.objects['Armature.026']

bpy.context.view_layer.objects.active = target_armature

# Get the bones from both armatures
source_bones = source_armature.pose.bones
target_bones = target_armature.pose.bones


#print("tO JE POZA KOSTI SOURCE")
#print(source_armature.pose.bones['Bone_1.002'].rotation_quaternion)
#print("tO JE POZA KOSTI TARGET")
#print(target_armature.pose.bones['Bone_1.002'].rotation_quaternion)

bone_pose = target_armature.pose.bones['Bone_0.002'].matrix.copy()

bpy.context.view_layer.objects.active = source_armature
source_armature.select_set(True)
bpy.ops.object.mode_set(mode='POSE')

bpy.ops.pose.select_all(action='SELECT')
bpy.ops.anim.keyframe_insert(type='BUILTIN_KSI_LocRot')

#bpy.ops.pose.select_all(action='SELECT')
#bpy.data.scenes['Scene'].frame_set(bpy.data.scenes['Scene'].frame_end)

source_armature.pose.bones['Bone_0.002'].matrix = bone_pose


bone_pose = target_armature.pose.bones['Bone_1.002'].matrix.copy()
source_armature.pose.bones['Bone_1.002'].matrix = bone_pose
#bpy.ops.anim.keyframe_insert(type='BUILTIN_KSI_LocRot')

#bpy.ops.object.posemode_toggle()
