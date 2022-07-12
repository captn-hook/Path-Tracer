import bpy
from bpy.types import Operator

class NAMES_Label(Operator):
    bl_idname = "names.label"
    bl_label = "Points"
    bl_description = "Places labels if Ds/Ts exist"

    @classmethod
    def poll(cls, context):
        try:
            pts = bpy.data.collections['[PT]Points']
            dsc = pts.children["[PT]D's"]
            tsc = pts.children["[PT]T's"]

            if len(dsc.all_objects) > 0 and len(tsc.all_objects) > 0:
                return True
            else:
                return False
        except:
            return False

    def execute(self, context):
        pts = bpy.data.collections['[PT]Points']
        dsc = pts.children["[PT]D's"]
        tsc = pts.children["[PT]T's"]

        bpy.ops.object.select_all(action='DESELECT')

        try:
            lbc = bpy.data.collections['[PT]Labels']
            
            for i in lbc.all_objects:
                i.select_set(True)
        
            bpy.ops.object.delete() 

        except KeyError:
            print("Making Label Collectino")
            #create point collections
            lbc = bpy.data.collections.new("[PT]Labels")
            bpy.context.scene.collection.children.link(lbc)

        def names(clc, lbc):
    
            for i in clc.all_objects:
                x, y, z = i.location[0], i.location[1], i.location[2]
                font_curve = bpy.data.curves.new(type="FONT", name=(i.name))
                font_curve.body = i.name
                font_obj = bpy.data.objects.new(name=i.name, object_data=font_curve)
                lbc.objects.link(font_obj)
                font_obj.location[0] = x
                font_obj.location[1] = y
                font_obj.location[2] = z + bpy.context.window_manager.height_cutoff

        names(dsc, lbc)
        names(tsc, lbc)

        return {'FINISHED'}
