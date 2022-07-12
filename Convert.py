<<<<<<< HEAD
import bpy
from bpy.types import Operator

class CONVERT_BW(Operator):
    bl_idname = "convert.bw"
    bl_label = "Convert BW"
    bl_description = "Convert selected objects to/from BW"

    @classmethod
    def poll(cls, context):
        if  len(bpy.context.selected_objects) > 0:
            return True
        else:
            return False

    def execute(self, context):
        for i in range(0, len(bpy.context.selected_objects)):
            mats = bpy.context.selected_objects[i].data.materials
            for i in range(0, len(mats)):
                nodes = mats[i].node_tree.nodes
                links = mats[i].node_tree.links

                bw = nodes.get('RGB to BW')

                if bw:
                    nodes.remove(bw)

                    image = nodes.get('Image Texture')
                    ps = nodes.get('Principled BSDF')
                    
                    links.new(image.outputs[0], ps.inputs[0])
        
                else:

                    image = nodes.get('Image Texture')
                    ps = nodes.get('Principled BSDF')
                    
                    new = nodes.new("ShaderNodeRGBToBW")
                    new.location = (0, 0)
                    new.label = "[PT]BW"
                    
                    tolink = [l for l in links if l.from_node == image and l.to_node == ps]
                    
                    link = tolink.pop()
                    links.new(link.from_node.outputs[0], new.inputs[0])
                    links.new(new.outputs[0], ps.inputs[0])
                    
        return {'FINISHED'}

class CONVERT_Shadow(Operator):
    bl_idname = "convert.shadow"
    bl_label = "Disable Shadows"
    bl_description = "Convert selected objects shadow"

    @classmethod
    def poll(cls, context):
        if  len(bpy.context.selected_objects) > 0:
            return True
        else:
            return False

    def execute(self, context):
        for obj in bpy.context.selected_objects:
            obj.visible_shadow = not obj.visible_shadow
            mats = obj.data.materials
            for mat in mats:
                if mat.shadow_method == 'NONE':
                    mat.shadow_method = 'OPAQUE'
                else:               
                    mat.shadow_method = 'NONE'
                
        return {'FINISHED'}

class CONVERT_Backface(Operator):
    bl_idname = "convert.backface"
    bl_label = "Disable Backface"
    bl_description = "Disable rendering of object backface."

    @classmethod
    def poll(cls, context):
        if  len(bpy.context.selected_objects) > 0:
            return True
        else:
            return False

    def execute(self, context):
        for obj in bpy.context.selected_objects:
            for mat in obj.data.materials:
                mat.use_backface_culling = not mat.use_backface_culling
                
=======
import bpy
from bpy.types import Operator

class CONVERT_BW(Operator):
    bl_idname = "convert.bw"
    bl_label = "Convert BW"
    bl_description = "Convert selected objects to/from BW"

    @classmethod
    def poll(cls, context):
        if  len(bpy.context.selected_objects) > 0:
            return True
        else:
            return False

    def execute(self, context):
        for i in range(0, len(bpy.context.selected_objects)):
            mats = bpy.context.selected_objects[i].data.materials
            for i in range(0, len(mats)):
                nodes = mats[i].node_tree.nodes
                links = mats[i].node_tree.links

                bw = nodes.get('RGB to BW')

                if bw:
                    nodes.remove(bw)

                    image = nodes.get('Image Texture')
                    ps = nodes.get('Principled BSDF')
                    
                    links.new(image.outputs[0], ps.inputs[0])
        
                else:

                    image = nodes.get('Image Texture')
                    ps = nodes.get('Principled BSDF')
                    
                    new = nodes.new("ShaderNodeRGBToBW")
                    new.location = (0, 0)
                    new.label = "[PT]BW"
                    
                    tolink = [l for l in links if l.from_node == image and l.to_node == ps]
                    
                    link = tolink.pop()
                    links.new(link.from_node.outputs[0], new.inputs[0])
                    links.new(new.outputs[0], ps.inputs[0])
                    
        return {'FINISHED'}

class CONVERT_Shadow(Operator):
    bl_idname = "convert.shadow"
    bl_label = "Disable Shadows"
    bl_description = "Convert selected objects shadow"

    @classmethod
    def poll(cls, context):
        if  len(bpy.context.selected_objects) > 0:
            return True
        else:
            return False

    def execute(self, context):
        for obj in bpy.context.selected_objects:
            obj.visible_shadow = not obj.visible_shadow
            mats = obj.data.materials
            for mat in mats:
                if mat.shadow_method == 'NONE':
                    mat.shadow_method = 'OPAQUE'
                else:               
                    mat.shadow_method = 'NONE'
                
        return {'FINISHED'}

class CONVERT_Backface(Operator):
    bl_idname = "convert.backface"
    bl_label = "Disable Backface"
    bl_description = "Disable rendering of object backface."

    @classmethod
    def poll(cls, context):
        if  len(bpy.context.selected_objects) > 0:
            return True
        else:
            return False

    def execute(self, context):
        for obj in bpy.context.selected_objects:
            for mat in obj.data.materials:
                mat.use_backface_culling = not mat.use_backface_culling
                
>>>>>>> 1e1229586b176ec78367bb9524d4dbb65313fb0e
        return {'FINISHED'}