# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name" : "PathTracer",
    "author" : "Tristan Hook",
    "description" : "Traces Paths",
    "blender" : (3, 2, 0),
    "version" : (1, 1, 2),
    "location" : "VIEW3D",
    "warning" : "",
    "category" : "Generic"
}

import bpy

from . Interface import INTERFACE_PT_Panel
from . Cursor import CURSOR_Location
from . Convert import CONVERT_BW
from . Convert import CONVERT_Backface
from . Convert import CONVERT_Shadow
from . Names import NAMES_Label
from . PT import OBJECT_Import
from . PT import SPAWN_DT
from . PT import BUILD_Tracers
from . PT import SPAWN_New
from . PT import SPAWN_Save

classes = (INTERFACE_PT_Panel, CURSOR_Location, NAMES_Label, OBJECT_Import, SPAWN_DT, SPAWN_Save, SPAWN_New, BUILD_Tracers, CONVERT_BW, CONVERT_Shadow, CONVERT_Backface)

def register():
    for c in classes:
        bpy.utils.register_class(c)

    win = bpy.types.WindowManager
    win.file_path = bpy.props.StringProperty(name="Data Path",
                                                            description="Data File path, forware slash seperated, from this file",     
                                                            default="/sampledata.txt")
    win.obj_path = bpy.props.StringProperty(name="Object Path",
                                                            description="Object file path, forware slash seperated, from this file",     
                                                            default="/matterpak\\building.obj")                                                                                                              
    win.pointsize = bpy.props.FloatProperty(name="Point Size",
                                                            description="D point numbering start",     
                                                            min=0, 
                                                            max=50, 
                                                            default=1)
    win.tracerwidth = bpy.props.FloatProperty(name="Tracer Width Mod",
                                                            description="Tracer width modifier",     
                                                            min=0, 
                                                            max=10, 
                                                            default=0.25)                                                        
    win.doff = bpy.props.IntProperty(name="D Offset",
                                                            description="D point numbering start",     
                                                            min=0, 
                                                            max=50, 
                                                            default=1)
    win.toff = bpy.props.IntProperty(name="T Offset",
                                                            description="T point numbering start",     
                                                            min=0, 
                                                            max=50, 
                                                            default=1)
    win.height_cutoff = bpy.props.FloatProperty(name="Cut",
                                                            description="Height in meters to boolean ceiling",     
                                                            min=-50, 
                                                            max=50, 
                                                            default=2.5)
    win.minopacity = bpy.props.FloatProperty(name="Opacity Mod",
                                                            description="Multiplier value",     
                                                            min=0, 
                                                            max=10, 
                                                            default=1)
    win.lift = bpy.props.FloatProperty(name="Lift",
                                                            description="Height in meters of center of tracer",     
                                                            min=0, 
                                                            max=50, 
                                                            default=3)
    win.headroom = bpy.props.FloatProperty(name="Headroom",
                                                            description="Distance in meters that each tr`acer will be to point",     
                                                            min=0, 
                                                            max=50, 
                                                            default=3)
    
    #groups
    #max = 100
    #groups = [0, 0.0005, 0.005, 0.02, .1, 0.5922612543706294, 1]
    #colors = ["#1e62b2","#70a8fa","#c4deff","#fd8181","#fd8181","#f91010","#d10000"]
    
    max = 25
    groups = [0,0.00016000640025601025,0.003960158406336254,0.01996079843193728,0.03996159846393856,0.1999679987199488,1]
    colors = ["#0000ff","#00a0ff","#02fbff","#4aff01","#fbfd00","#ff5a00","#ff0000"]

    opacity = [0, .1, .2, .4, .6, .8, 1]
    scale = [0, .1, .2, .4, .6, .8, 1]

    for i in range(0, len(colors)):
        h = colors[i].lstrip('#')
        colors[i] = tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
        colors[i] = (colors[i][0] / 256, colors[i][1] / 256, colors[i][2] / 256)
        
        #opacity[i] = groups[i]
        #scale[i] = groups[i] * 3
        scale[i] = scale[i] * 3
    print(colors)
        
    
    win.br1 = bpy.props.FloatProperty(name="",
                                                            description="Data breakpoint 1",     
                                                            min=0, 
                                                            max=100, 
                                                            default=groups[0] * max)
    win.br2 = bpy.props.FloatProperty(name="",
                                                            description="Data breakpoint 2",     
                                                            min=0, 
                                                            max=100, 
                                                            default=groups[1] * max)                                                                                                                
    win.br3 = bpy.props.FloatProperty(name="",
                                                            description="Data breakpoint 3",     
                                                            min=0, 
                                                            max=100, 
                                                            default=groups[2]* max)
    win.br4 = bpy.props.FloatProperty(name="",
                                                            description="Data breakpoint 4",     
                                                            min=0, 
                                                            max=100, 
                                                            default=groups[3]* max)
    win.br5 = bpy.props.FloatProperty(name="",
                                                            description="Data breakpoint 5",     
                                                            min=0, 
                                                            max=100, 
                                                            default=groups[4]* max)                                                                                                                
    win.br6 = bpy.props.FloatProperty(name="",
                                                            description="Data breakpoint 6",     
                                                            min=0, 
                                                            max=100, 
                                                            default=groups[5]* max)
    win.br7 = bpy.props.FloatProperty(name="",
                                                            description="Data breakpoint 7",     
                                                            min=0, 
                                                            max=100, 
                                                            default=groups[6]* max)                                                        

    #opacity
    win.op1 = bpy.props.FloatProperty(name="",
                                                            description="Opacity Breakpoint 1",     
                                                            min=0, 
                                                            max=1, 
                                                            default=opacity[0])
    win.op2 = bpy.props.FloatProperty(name="",
                                                            description="Opacity Breakpoint 2",     
                                                            min=0, 
                                                            max=1, 
                                                            default=opacity[1])
    win.op3 = bpy.props.FloatProperty(name="",
                                                            description="Opacity Breakpoint 3",     
                                                            min=0, 
                                                            max=1, 
                                                            default=opacity[2])
    win.op4 = bpy.props.FloatProperty(name="",
                                                            description="Opacity Breakpoint 4",     
                                                            min=0, 
                                                            max=1, 
                                                            default=opacity[3])
    win.op5 = bpy.props.FloatProperty(name="",
                                                            description="Opacity Breakpoint 5",     
                                                            min=0, 
                                                            max=1, 
                                                            default=opacity[4])
    win.op6 = bpy.props.FloatProperty(name="",
                                                            description="Opacity Breakpoint 6",     
                                                            min=0, 
                                                            max=1, 
                                                            default=opacity[5])
    win.op7 = bpy.props.FloatProperty(name="",
                                                            description="Opacity Breakpoint 7",     
                                                            min=0, 
                                                            max=1, 
                                                            default=opacity[6])

    #scale
    win.sc1 = bpy.props.FloatProperty(name="",
                                                            description="Scale Breakpoint 1",     
                                                            min=0.01, 
                                                            max=10, 
                                                            default=scale[0])
    win.sc2 = bpy.props.FloatProperty(name="",
                                                            description="Scale Breakpoint 2",     
                                                            min=0.01, 
                                                            max=10, 
                                                            default=scale[1])                                                        
    win.sc3 = bpy.props.FloatProperty(name="",
                                                            description="Scale Breakpoint 3",     
                                                            min=0.01, 
                                                            max=10, 
                                                            default=scale[2])
    win.sc4 = bpy.props.FloatProperty(name="",
                                                            description="Scale Breakpoint 4",     
                                                            min=0.1, 
                                                            max=10, 
                                                            default=scale[3])
    win.sc5 = bpy.props.FloatProperty(name="",
                                                            description="Scale Breakpoint 5",     
                                                            min=0.1, 
                                                            max=10, 
                                                            default=scale[4])                                                        
    win.sc6 = bpy.props.FloatProperty(name="",
                                                            description="Scale Breakpoint 6",     
                                                            min=0.1, 
                                                            max=10, 
                                                            default=scale[5])
    win.sc7 = bpy.props.FloatProperty(name="",
                                                            description="Scale Breakpoint 7",     
                                                            min=0.1, 
                                                            max=10, 
                                                            default=scale[6])
    #color groups
    win.color1 = bpy.props.FloatVectorProperty(name='Color 1', 
                                                                    description='Arrow Color 1',
                                                                    min=0,
                                                                    max=1,
                                                                    default=colors[0],
                                                                    subtype='COLOR')
    win.color2 = bpy.props.FloatVectorProperty(name='Color 2', 
                                                                    description='Arrow Color 2',
                                                                    min=0,
                                                                    max=1,
                                                                    default=colors[1],
                                                                    subtype='COLOR')
    win.color3 = bpy.props.FloatVectorProperty(name='Color 3', 
                                                                    description='Arrow Color 3',
                                                                    min=0,
                                                                    max=1,
                                                                    default=colors[2],
                                                                    subtype='COLOR')
    win.color4 = bpy.props.FloatVectorProperty(name='Color 4', 
                                                                    description='Arrow Color 4',
                                                                    min=0,
                                                                    max=1,
                                                                    default=colors[3],
                                                                    subtype='COLOR')
    win.color5 = bpy.props.FloatVectorProperty(name='Color 5', 
                                                                    description='Arrow Color 5',
                                                                    min=0,
                                                                    max=1,
                                                                    default=colors[4],
                                                                    subtype='COLOR')
    win.color6 = bpy.props.FloatVectorProperty(name='Color 6', 
                                                                    description='Arrow Color 6',
                                                                    min=0,
                                                                    max=1,
                                                                    default=colors[5],
                                                                    subtype='COLOR')
    win.color7 = bpy.props.FloatVectorProperty(name='Color 7', 
                                                                    description='Arrow Color 6',
                                                                    min=0,
                                                                    max=1,
                                                                    default=colors[6],
                                                                    subtype='COLOR')                                                                

    #point color
    win.dcolor = bpy.props.FloatVectorProperty(name='D color', 
                                                                    description='Arrow Color 5',
                                                                    min=0,
                                                                    max=1,
                                                                    default=(1, .25, .25),
                                                                    subtype='COLOR')
    win.tcolor = bpy.props.FloatVectorProperty(name='T color', 
                                                                    description='Arrow Color 6',
                                                                    min=0,
                                                                    max=1,
                                                                    default=(.25, .25, 1),
                                                                    subtype='COLOR')

    win.nullcolor = bpy.props.FloatVectorProperty(name='Null Color', 
                                                                    description='Null Arrow Color 6',
                                                                    min=0,
                                                                    max=1,
                                                                    default=(1, 1, 1),
                                                                    subtype='COLOR')
                                                
def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)
    win = bpy.types.WindowManager
    del win.file_path
    del win.obj_path
    del win.pointsize
    del win.tracerwidth
    del win.doff
    del win.toff
    del win.height_cutoff
    del win.minopacity
    del win.lift
    del win.headroom

    del win.br1
    del win.br2
    del win.br3
    del win.br4
    del win.br5
    del win.br6

    del win.sc1
    del win.sc2
    del win.sc3
    del win.sc4
    del win.sc5
    del win.sc6

    del win.color1
    del win.color2
    del win.color3
    del win.color4
    del win.color5
    del win.color6

    del win.dcolor
    del win.tcolor

