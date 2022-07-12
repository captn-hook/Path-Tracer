import bpy
from bpy.types import Operator

class CURSOR_Location(Operator):
    bl_idname = "cursor.location"
    bl_label = "X, Y, Z"
    bl_description = "Prints location of 3D cursor"

    @classmethod
    def poll(cls, context):
        if bpy.context.workspace.tools.from_space_view3d_mode('OBJECT', create=False).idname == 'builtin.cursor':
            return True
        else:
            return False

    def execute(self, context):
        x = bpy.context.scene.cursor.location[0]
        y = bpy.context.scene.cursor.location[1]
        z = bpy.context.scene.cursor.location[2]

        print("({:0.2f}, ".format(x) + "{:0.2f}, ".format(y) + "{:0.2f}) ".format(z))

        return {'FINISHED'}