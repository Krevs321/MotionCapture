import bpy

bpy.ops.object.armature_add(enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
bpy.data.objects['Armature']

bpy.ops.object.editmode_toggle()

pointX = [0.5, 2]
pointY = [1, -0.5]        
pointZ = [2, -1]

for i in range(len(pointX)):
    bpy.ops.armature.extrude_move(ARMATURE_OT_extrude={"forked":False}, TRANSFORM_OT_translate={"value":(pointX[i], pointY[i], pointZ[i]), "orient_axis_ortho":'X', "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "view2d_edge_pan":False, "release_confirm":False, "use_accurate":False, "use_automerge_and_split":False})
   

arm = bpy.data.armatures['Armature']
bpy.ops.object.mode_set(mode='OBJECT') # .select only has an effect in object mode (don't ask me why)
for bone in arm.bones: # deselect the other bones
    bone.select = False
    bone.select_tail = False
    bone.select_head = False

arm.bones['Bone'].select_tail = True
bpy.ops.object.mode_set(mode='EDIT')