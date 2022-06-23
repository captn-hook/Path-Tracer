import bpy 

print(len(bpy.data.materials))

for i in range(0, len(bpy.data.materials)):
    #bpy.data.materials[i].node_tree.nodes["Principled BSDF"].inputs[21].default_value  = 1
    print(bpy.data.materials[i])
    bpy.data.materials[i].use_backface_culling = True
    bpy.data.materials[i].shadow_method = "NONE"
    
for i in range(0, len(bpy.data.objects)):
    #bpy.data.materials[i].node_tree.nodes["Principled BSDF"].inputs[21].default_value  = 1
    print(bpy.data.objects[i])
    bpy.data.objects[i].ray_visibility = False