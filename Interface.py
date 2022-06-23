from sqlite3 import Row
import bpy

from bpy.types import Panel

class INTERFACE_PT_Panel(Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "PathTracer"
    bl_category = "PT"
    bl_idname = "INTERFACE_PT_Panel"

    def draw(self, context):    

        layout = self.layout
        layout.label(text= "External Files:")
        row = layout.row()
        layout.prop(context.window_manager, "file_path")
        row = layout.row()
        layout.prop(context.window_manager, "obj_path")
        

        layout.label(text= "Commands:")
        row = layout.row()
        row.operator("cursor.location", text = "Get Cursor XYZ", icon='WORLD_DATA')
        row.operator("convert.bw", text = "Convert to/from B&W", icon='WORLD_DATA')
        row.operator("names.label", text = "Create Labels", icon='WORLD_DATA')
        row = layout.row()
        row.operator("convert.shadow", text = "Disable/Enable shadows", icon='WORLD_DATA')
        row.operator("convert.backface", text = "Disable/Enable backface culling", icon='WORLD_DATA')


        layout.label(text= "Import:")
        row = layout.row()
        row.operator("import.obj", text = "Import OBJ", icon='WORLD_DATA')
        row.prop(context.window_manager, "height_cutoff")

        
        layout.label(text= "Points:")
        row = layout.row()
        row.operator("spawn.dt", text = "Spawn Points", icon='WORLD_DATA')
        row.prop(context.window_manager, "pointsize")
        row = layout.row()
        row.prop(context.window_manager, "doff")
        row.prop(context.window_manager, "toff")

        row = layout.row()
        row.prop(context.window_manager, "dcolor")
        row.prop(context.window_manager, "tcolor")

        row = layout.row()
        row.operator("spawn.new", text = "Spawn New Points", icon='WORLD_DATA')
        row.operator("spawn.save", text = "Save Points", icon='WORLD_DATA')
    
        layout.label(text= "Tracers:")
        row = layout.row()
        row.operator("build.tracers", text = "Build Tracers", icon='WORLD_DATA')
        row = layout.row()
        row.prop(context.window_manager, "tracerwidth")
        row.prop(context.window_manager, "minopacity")
        row = layout.row()
        row.prop(context.window_manager, "lift")
        row.prop(context.window_manager, "headroom")

        layout.label(text= "Value Breakpoints:")
        row = layout.row()
        row.prop(context.window_manager, "br1")
        row.prop(context.window_manager, "br2")
        row.prop(context.window_manager, "br3")
        row.prop(context.window_manager, "br4")
        row.prop(context.window_manager, "br5")
        row.prop(context.window_manager, "br6")
        row.prop(context.window_manager, "br7")

        layout.label(text= "Opacity Breakpoints:")
        row = layout.row()
        row.prop(context.window_manager, "op1")
        row.prop(context.window_manager, "op2")
        row.prop(context.window_manager, "op3")
        row.prop(context.window_manager, "op4")
        row.prop(context.window_manager, "op5")
        row.prop(context.window_manager, "op6")
        row.prop(context.window_manager, "op7")

        layout.label(text= "Scale Breakpoints:")
        row = layout.row()
        row.prop(context.window_manager, "sc1")
        row.prop(context.window_manager, "sc2")
        row.prop(context.window_manager, "sc3")
        row.prop(context.window_manager, "sc4")
        row.prop(context.window_manager, "sc5")
        row.prop(context.window_manager, "sc6")
        row.prop(context.window_manager, "sc7")

        layout.label(text= "Color Settings:")
        row = layout.row()
        layout.prop(context.window_manager, "color1")
        layout.prop(context.window_manager, "color2")
        layout.prop(context.window_manager, "color3")
        layout.prop(context.window_manager, "color4")
        layout.prop(context.window_manager, "color5")
        layout.prop(context.window_manager, "color6")
        layout.prop(context.window_manager, "color7")
        layout.prop(context.window_manager, "nullcolor")