#////////////////////////
#////////////////////////
#by tristan hook 1/26/2022
#4/19/2022
#////////////////////////
#////////////////////////

from operator import truediv
import bpy
import bmesh
import math
import random
from bpy.types import Operator
from pathlib import Path
from mathutils import Vector
import csv

#Disables class polling in PT classes
devmode = False

#////////////////////////
#imports .obj
#////////////////////////

class OBJECT_Import(Operator):
    bl_idname = "import.obj"
    bl_label = "Import"
    bl_description = "Specify file"

    @classmethod
    def poll(cls, context):
        try:
            file = fixfile(bpy.context.window_manager.obj_path)
            lines = open(file, "r")
            return True
        except FileNotFoundError:
            return devmode
        
    def execute(self, context):
        resetSelection()

        #removes old uncollected bg
        if len(bpy.data.scenes[0].collection.all_objects) >= 0:
            for i in bpy.data.scenes[0].collection.all_objects:

                if len(i.name) >= 8 and "[PT][BG]" == i.name[0:8]:
                    bpy.data.objects.remove(i, do_unlink=True)
                
                elif len(i.name) >= 10 and "[PT]cutobj" == i.name[0:10]:
                    bpy.data.objects.remove(i, do_unlink=True)
            
        file = fixfile(bpy.context.window_manager.obj_path)
        obj = importmatterport(file)

        cut(bpy.context.window_manager.height_cutoff, obj)

        return {'FINISHED'}

#////////////////////////
#spawns points 
#two spawning classes / one respawns / one saves
#////////////////////////

class SPAWN_DT(Operator):
    bl_idname = "spawn.dt"
    bl_label = "Spawn"
    bl_description = "Specify file"

    @classmethod
    def poll(cls, context):
        try:
            file = fixfile(bpy.context.window_manager.file_path)
            lines = open(file, "r")
            return True
        except FileNotFoundError:
            return devmode

    def execute(self, context):
        resetSelection()

        file = fixfile(bpy.context.window_manager.file_path)
        dspawn, tspawn, transmission = datafile(file)
        try:
            pts = bpy.data.collections['[PT]Points']
            dsc = bpy.data.collections['[PT]Points'].children["[PT]D's"]
            tsc = bpy.data.collections['[PT]Points'].children["[PT]T's"]
            empty(dsc)
            empty(tsc)
        except KeyError:
            print("Making point collections")
            #create point collections
            pts = bpy.data.collections.new("[PT]Points")
            bpy.context.scene.collection.children.link(pts)
    
            dsc = bpy.data.collections.new("[PT]D's")
            pts.children.link(dsc)
    
            tsc = bpy.data.collections.new("[PT]T's")
            pts.children.link(tsc)
    
        spawn(dspawn, dsc, True)
        spawn(tspawn, tsc, False) 

        return {'FINISHED'}

class SPAWN_New(Operator):
    bl_idname = "spawn.new"
    bl_label = "Spawn new points"
    bl_description = "Duplicate points in collection and save"

    @classmethod
    def poll(cls, context):
        try:
            pts = bpy.data.collections['[PT]Points']
            dsc = bpy.data.collections['[PT]Points'].children["[PT]D's"]
            tsc = bpy.data.collections['[PT]Points'].children["[PT]T's"]

            if len(dsc.all_objects) == 0 and len(tsc.all_objects) == 0:
                return True
            else:
                return devmode
        except KeyError:
            return True

    def execute(self, context):
        resetSelection()

        try:
            pts = bpy.data.collections['[PT]Points']
            dsc = bpy.data.collections['[PT]Points'].children["[PT]D's"]
            tsc = bpy.data.collections['[PT]Points'].children["[PT]T's"]
        except KeyError:
            print("Making point collections")
            #create point collections
            pts = bpy.data.collections.new("[PT]Points")
            bpy.context.scene.collection.children.link(pts)
    
            dsc = bpy.data.collections.new("[PT]D's")
            pts.children.link(dsc)
    
            tsc = bpy.data.collections.new("[PT]T's")
            pts.children.link(tsc)
    
        spawn([(-1, 0, 0)], dsc, True)
        spawn([(1, 0, 0)], tsc, False) 

        return {'FINISHED'}

class SPAWN_Save(Operator):
    bl_idname = "spawn.save"
    bl_label = "Save"
    bl_description = "Specify file"

    @classmethod
    def poll(cls, context):
        try:
            pts = bpy.data.collections['[PT]Points']
            dsc = bpy.data.collections['[PT]Points'].children["[PT]D's"]
            tsc = bpy.data.collections['[PT]Points'].children["[PT]T's"]

            if len(dsc.all_objects) > 0 and len(tsc.all_objects) > 0:
                return True
            else:
                return devmode
        except KeyError:
            return devmode

    def execute(self, context):
        resetSelection()

        dsc = bpy.data.collections['[PT]Points'].children["[PT]D's"]
        tsc = bpy.data.collections['[PT]Points'].children["[PT]T's"]

        try:
            file = fixfile(bpy.context.window_manager.file_path)
            dspawn, tspawn, transmission = datafile(file)

        except FileNotFoundError:
            print("Filling with 0 data")
            transmission = [0] * (len(dsc.all_objects) * len(tsc.all_objects))
        
        dspawn, tspawn = newPosList(dsc, tsc)

        file = open(file, 'w')
       
        if bpy.context.window_manager.file_path[-4:] == ".csv":
            
            file.write("TRNS,")

            for i in range(0, len(dspawn)):
                file.write(dspawn[i])

                if i < len(dspawn) - 1:
                    file.write(",")

            file.write("\n")

            for n in range(0, len(tspawn)):
                file.write(tspawn[n] + ",")
                
                for i in range(0, len(dspawn)):
                    file.write(str(transmission[i + n * len(dspawn)]))

                    if i < len(dspawn) - 1:
                        file.write(",")
                
                file.write("\n")
            
            return {'FINISHED'}
            
        elif bpy.context.window_manager.file_path[-4:] == ".txt":   

            file.write("Ds\n")

            for i in dspawn:
                file.write(str(i)+"\n")

            file.write('\n')
            file.write("Ts\n")

            for i in tspawn:
                file.write(str(i)+"\n")

            file.write('\n')
            file.write("Transmission\n")

            for i in transmission:
                file.write(str(i)+"\n")

            return {'FINISHED'}
#////////////////////////
#Spawns Tracers
#////////////////////////

class BUILD_Tracers(Operator):
    bl_idname = "build.tracers"
    bl_label = "Build Tracers"
    bl_description = "Specify File"

    @classmethod
    def poll(cls, context):
        try:
            file = fixfile(bpy.context.window_manager.file_path)
            lines = open(file, "r")
            return True
        except FileNotFoundError:
            return devmode

    def execute(self, context):
        resetSelection()
        try:
            arw = bpy.data.collections['[PT]Tracers']
            crv = bpy.data.collections['[PT]Tracers'].children['[PT]Curves']

        except:

            print("Making tracer collections")
            #create tracer collections
            arw = bpy.data.collections.new("[PT]Tracers")
            bpy.context.scene.collection.children.link(arw)
    
            crv = bpy.data.collections.new("[PT]Curves")
            arw.children.link(crv)

            #https://blenderartists.org/t/disable-exlude-from-view-layer-in-collection/1324744
            def recurLayerCollection(layerColl, collName):
                found = None
                if (layerColl.name == collName):
                    return layerColl
                for layer in layerColl.children:
                    found = recurLayerCollection(layer, collName)
                    if found:
                        return found

            #layer_collection = bpy.context.view_layer.layer_collection
            #use view_layer 0 instead of context
            layer_collection = bpy.data.scenes[0].view_layers[0].layer_collection
            layerColl = recurLayerCollection(layer_collection, crv.name)
            bpy.context.view_layer.active_layer_collection = layerColl

            bpy.context.view_layer.active_layer_collection.exclude = True

            resetSelection()

        file = fixfile(bpy.context.window_manager.file_path)
        tracers(file, crv, arw)

        return {'FINISHED'}

def importmatterport(path):            
    bpy.ops.object.select_all(action='DESELECT')
    axis0 = ('X', 'Z')
    axis1 = ('Z', 'Y')
    axis2 = ('Y', 'X')
    bpy.ops.import_scene.obj(filepath = path, filter_glob = '*.obj;*.mtl', use_image_search = True, split_mode = 'ON', axis_forward = axis0[0], axis_up = axis0[1])
    bpy.ops.object.transform_apply(rotation=True)

    importdOBJ = bpy.context.selected_objects[0]
    importdOBJ.name = "[PT][BG]" + importdOBJ.name
    return importdOBJ

def empty(clc):
    bpy.ops.object.select_all(action='DESELECT')
    
    for i in clc.all_objects:
        i.select_set(True)
        
    bpy.ops.object.delete() 
        
def cut(z, importdOBJ):
    #make bounding cube
    bbox_corners = [importdOBJ.matrix_world @ Vector(corner) for corner in importdOBJ.bound_box]
    verts = bbox_corners
    faces = [(0, 1, 2, 3), (4, 7, 6, 5), (0, 4, 5, 1), (1, 5, 6, 2), (2, 6, 7, 3), (4, 0, 3, 7)]

    #assemble cube
    mesh = bpy.data.meshes.new('cubemesh')
    mesh.from_pydata(verts, [], faces)
    cube = bpy.data.objects.new('[PT]cutobj', mesh)

    cube.scale[0] = cube.scale[0] * 1.1
    cube.scale[1] = cube.scale[1]* 1.1
    cube.location[2] = cube.location[2] + z

    #boolean operation
    bpy.context.view_layer.objects.active = importdOBJ
    bpy.ops.object.modifier_add(type = 'BOOLEAN')
    importdOBJ.modifiers["Boolean"].operation = 'DIFFERENCE'
    importdOBJ.modifiers["Boolean"].use_self = True
    importdOBJ.modifiers["Boolean"].object = cube
        
    #hide cube
    bpy.context.scene.collection.objects.link(cube)
    cube.parent = importdOBJ

    cube.hide_set(True)
    cube.hide_render = True
        
    return cube

def resetSelection():
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.view_layer.active_layer_collection = bpy.data.scenes[0].view_layers[0].layer_collection

#///////////////data file functions
def transmissionTranspose(trans, columns):

    transmission = []

    print(len(trans) / columns)
    for n in range(0, columns):
        for i in range(0, int(len(trans) / columns)):
            transmission.append(trans[columns * i + n])

    print(trans)
    print(transmission)
    return transmission

def newPosList(dsc, tsc):

    dspawn = []
    tspawn = []


    for i in dsc.all_objects:
        print(i.name)
        x = i.location[0]
        y = i.location[1]
        z = i.location[2]
        dspawn.append(str(x) + "/" + str(y) + "/" + str(z))

    for i in tsc.all_objects:
        print(i.name)
        x = i.location[0]
        y = i.location[1]
        z = i.location[2]
        tspawn.append(str(x) + "/" + str(y) + "/" + str(z))

    return dspawn, tspawn


def fixfile(file):
    if file[0] == "/":
        return bpy.path.abspath(r"//" + file[1:])
    else:
        return bpy.path.abspath(file)

def look_at(obj_camera, loc, point):
    #https://blender.stackexchange.com/questions/5210/pointing-the-camera-in-a-particular-direction-programmatically
    loc_camera = Vector(loc) # obj_camera.matrix_world.to_translation()

    point = Vector(point) # target location
    print(point, loc_camera)
    
    direction = point - loc_camera
    # point the cameras '-Z' and use its 'Y' as up
    rot_quat = direction.to_track_quat('-Z', 'Y')

    # assume we're using euler rotation
    obj_camera.rotation_euler = rot_quat.to_euler()

def datafile(datafilename):
    print("Data from", datafilename)
    line_count = 0
    lines = open(datafilename, "r")
    
    #assign data blocks
    dspawn = []
    tspawn = []
    transmission = []

    if bpy.context.window_manager.file_path[-4:] == ".csv":
        # TRNS,-80/14/-2,-107/27/-2,99/-27/-2
        # -78/-9/-2,1,2,3
        # 78/-17/2,4,5,6
        # -87/-14/-2,7,8,9
    
        twodarray = []
        length = 0

        with open(datafilename) as csv_file2:
            csv_reader2 = csv.reader(csv_file2, delimiter=',')
            for row in csv_reader2:
                twodarray.append(row)
                length += 1
                

        with open(datafilename) as csv_file:
            #get number of rows
            
            csv_reader = csv.reader(csv_file, delimiter=',')

            
            if twodarray[0][0] == "Labels":
                print("Labels", csv_reader)
                #first row and column are labels, second row and column are coordinates except for 1,1 which is coordinate system
                #second to last row is INSIGHTS, not needed
                #last row is views, spawn animated camera with keyframes at each view

                for row in csv_reader:
                    print(line_count)
                    if line_count == 0:
                        #skip
                        pass
                    elif line_count == 1:
                        #get dspawn
                        print(row)
                        for i in range(2, len(row)):
                            print(row[i])
                            x, y, z = tuple(map(float, row[i].split('/')))
                            dspawn.append((x, y * -1, z))    
                    #while not at last two rows
                    elif line_count < length - 2:
                        #get tspawn
                        x, y, z = tuple(map(float, row[1].split('/')))
                        tspawn.append((x, y * -1, z))
                        #get transmission
                        for i in range(2, len(row)):
                            transmission.append(row[i])
                    #do camera stuff
                    elif line_count == length - 1:
                        camera_coords = []
                        for i in range(1, len(row)):
                            x, y, z = tuple(map(float, row[i].split('/')))
                            camera_coords.append((x, y * -1, z))
                        print("making camera")
                        #spawn camera
                        camera_data = bpy.data.cameras.new(name='Camera')
                        camera_object = bpy.data.objects.new('Camera', camera_data)
                        camera_object.rotation_mode = 'XYZ'
                        bpy.context.scene.collection.objects.link(camera_object)
                        #set keyframes
                        for i in range(len(camera_coords)):
                            camera_object.location = camera_coords[i]
                            camera_object.keyframe_insert(data_path="location", frame=i)
                            #lookat dspawn
                            print("looking at", dspawn[i], "from", camera_coords[i])
                            look_at(camera_object, camera_coords[i], dspawn[i])
                            camera_object.keyframe_insert(data_path="rotation_euler", frame=i)
                            
                    line_count += 1

                print(line_count, length)
                print(dspawn, tspawn, transmission)
                
                return dspawn, tspawn, transmission
                        
            else:
                for row in csv_reader:
                    if line_count == 0:
                        #range 1 to len(row) to skip the first cell
                        for i in range(1, len(row)):

                            if "/" in row[i]:
                                x, y, z = tuple(map(float, row[i].split('/')))

                            else:
                                print(row[i] + " NOT A LOCATION")
                                x, y, z = (0.0, 0.0, 0.0)
                            #check if this * -1 is needed
                            dspawn.append((x,  y * -1, z))

                    else:
                        #lines after 0 are coord,transmission,transmission,transmission,...
                        for i in range(0, len(row)):
                            if i == 0:

                                if "/" in row[i]:
                                    x, y, z = tuple(map(float, row[i].split('/')))

                                else:
                                    print(row[i] + " NOT A LOCATION")
                                    x, y, z = (0.0, 0.0, 0.0)

                                tspawn.append((x, y * -1, z))
                                
                            else:
                                transmission.append(row[i])

                    line_count += 1
                
                
                transmission = transmissionTranspose(transmission, len(dspawn))
                
                return dspawn, tspawn, transmission

    elif bpy.context.window_manager.file_path[-4:] == ".txt":
        #find data blocks
        for line in lines:
            if line == "Ds\n":
                dstart = line_count + 1
            elif line == "Ts\n":
                dend = line_count - 2
                tstart = line_count + 1
            elif line == "Transmission\n":
                tend = line_count - 2
                transstart = line_count + 1
            line_count += 1
        transend = line_count
#/Path-Tracer/sample.txt

        i = 0
        lines = open(datafilename, "r")

        for line in lines:
            #strip \n
            line = line.strip()
            if dstart <= i <= dend:
                line = tuple(map(float, line.split('/')))
                dspawn.append(line)
            if tstart <= i <= tend:
                print(line)
                line = tuple(map(float, line.split('/')))
                tspawn.append(line)
            if transstart <= i <= transend:
                line = float(line)
                transmission.append(line)
            i += 1

        print('dspawn', dspawn)
        print('tspawn', tspawn)
        print('transmission', transmission)
        return dspawn, tspawn, transmission
    else:
        print("DATAFILE ERROR")
#////////////////////////
#spawns d's and t's
#////////////////////////
    
#places D and T points
def spawn(spawns, clc, dt):
    list = []

    dmat = bpy.data.materials.new(name = str("D Mat"))
    dmat.use_nodes = True
    dmat.shadow_method = 'NONE'
    dmat.node_tree.nodes["Principled BSDF"].inputs['Base Color'].default_value = (bpy.context.window_manager.dcolor[0], bpy.context.window_manager.dcolor[1], bpy.context.window_manager.dcolor[2], 1)          
    tmat = bpy.data.materials.new(name = str("T Mat"))
    tmat.use_nodes = True
    tmat.shadow_method = 'NONE'
    tmat.node_tree.nodes["Principled BSDF"].inputs['Base Color'].default_value = (bpy.context.window_manager.tcolor[0], bpy.context.window_manager.tcolor[1], bpy.context.window_manager.tcolor[2], 1)
          
        
      
    for i in range(len(spawns)):
         
        x, y, z = spawns[i]
        
        if dt:
            bpy.ops.mesh.primitive_cylinder_add(location=(x, y, z), depth=(bpy.context.window_manager.pointsize * 0.4), radius=(bpy.context.window_manager.pointsize * 0.4))
        else:
            bpy.ops.mesh.primitive_cube_add(location=(x, y, z), size=(bpy.context.window_manager.pointsize * 0.5))
        
        new = bpy.context.active_object

        new.scale[2] = new.scale[2] * 0.5

        list.append(new)
         
        new.name = str(("D" if dt else "T") + str(i + (bpy.context.window_manager.doff if dt else bpy.context.window_manager.toff)))
        
        new.data.materials.append(dmat if dt else tmat)

        clc.objects.link(new)
        bpy.context.scene.collection.objects.unlink(new)

    return list    

#/////////////////data interpretation / spawning funcs

def rescale(val, inmin, inmax, outmin, outmax):
    return outmin + (val - inmin) * ((outmax - outmin) / (inmax - inmin))
                
def midpoint(x1, y1, z1, x2, y2, z2):
    
    x = (x1 + x2) / 2
    y = (y1 + y2) / 2
    z = (z1 + z2) / 2
    
    return x, y, z

def zlift(lift, length):
    if length > 15:
        return lift
    else:
        return lift / 2
          
def rgb(value):
    #THIS IS WHAT DECIDES HOW DATA IS SHOWN
    groups = [bpy.context.window_manager.br1, bpy.context.window_manager.br2, bpy.context.window_manager.br3, bpy.context.window_manager.br4, bpy.context.window_manager.br5, bpy.context.window_manager.br6, bpy.context.window_manager.br7]
    colors = [bpy.context.window_manager.color1, bpy.context.window_manager.color2, bpy.context.window_manager.color3, bpy.context.window_manager.color4, bpy.context.window_manager.color5, bpy.context.window_manager.color6, bpy.context.window_manager.color7]
    opacity = [bpy.context.window_manager.op1, bpy.context.window_manager.op2, bpy.context.window_manager.op3, bpy.context.window_manager.op4, bpy.context.window_manager.op5, bpy.context.window_manager.op6, bpy.context.window_manager.op7]
    scale = [bpy.context.window_manager.sc1, bpy.context.window_manager.sc2, bpy.context.window_manager.sc3, bpy.context.window_manager.sc4, bpy.context.window_manager.sc5, bpy.context.window_manager.sc6, bpy.context.window_manager.sc7]

    for i in range(len(groups)):
        
        #if i + 1 == len(groups):
        #    r, g, b = colors[len(groups) - 1\]
        #    return r, g, b, scale[len(groups) - 1], opacity[len(groups) - 1], len(groups) - 1

        #groups[0] <= value <= groups[-1] and

        if groups[i] <= value <= groups[i + 1]:
            collector = i
                
            r1, g1, b1 = colors[i]
            r2, g2, b2 = colors[i + 1]
                
            r = rescale(value, groups[i], groups[i + 1], r1, r2)
            g = rescale(value, groups[i], groups[i + 1], g1, g2)
            b = rescale(value, groups[i], groups[i + 1], b1, b2)
                
            scale = rescale(value, groups[i], groups[i + 1], scale[i], scale[i + 1])
            opacity = rescale(value, groups[i], groups[i + 1], opacity[i], opacity[i + 1])
                
            if opacity * bpy.context.window_manager.minopacity <= 1:
                opacity = opacity * bpy.context.window_manager.minopacity
            else:
                opacity = 1

            return r, g, b, scale, opacity, collector

        elif value > groups[len(groups) - 1]:
            r, g, b = colors[len(groups) - 1]
            return r, g, b, scale[len(groups) - 1], opacity[len(groups) - 1], i
    
    return bpy.context.window_manager.nullcolor[0], bpy.context.window_manager.nullcolor[1], bpy.context.window_manager.nullcolor[2], bpy.context.window_manager.tracerwidth, bpy.context.window_manager.minopacity, 0
    
#////////////////////////
#tracers
#////////////////////////

def tracers(file, crv, arw):
    #connect every d to its t, mainy body loop
    dspawn, tspawn, transmission = datafile(file)

    insig = []
    counter = 0
    for ds in range(len(dspawn)):
        
        dclc = bpy.data.collections.new("[PT]D" + str(ds + 1))
        arw.children.link(dclc)

        for ts in range(len(tspawn)):
            
            #map coords
            name = "D " + str(bpy.context.window_manager.doff + ds) + " T " + str(bpy.context.window_manager.toff + ts)
            
            curve = None

            #find existing curves
            if len(crv.all_objects) > 0:
                for i in crv.all_objects:    
                    if i.name.count(" ") == 3:
                        dname, d, tname, t = i.name.split(" ")
                        if t.count(".") > 0:
                            t, tail = t.split(".")
                        if int(d) == ds + bpy.context.window_manager.doff and int(t) == ts + bpy.context.window_manager.toff:
                            curve = i
            
            if curve:
                print("Found existing curve", curve.name)
            else:
                curve = createCurve(name, crv, dspawn[ds], tspawn[ts])

            r, g, b, scale, opacity, collector = rgb(float(transmission[counter]))

            print("DS, TS, R, G, B, S, O, T")
            print(ds, ts, r, g, b, scale, opacity, transmission[counter])

            scale = scale * bpy.context.window_manager.tracerwidth

            #duplicate arrow to each
            bpy.ops.mesh.primitive_plane_add(size=scale, enter_editmode=False, location=(0, 0, 0), scale=(0.0, 0.0, 0.0))
            bpy.ops.object.modifier_add(type='ARRAY')
            bpy.ops.object.modifier_add(type='CURVE')

            arrow = bpy.context.active_object
            arrow.modifiers["Array"].fit_type = 'FIT_LENGTH'
            arrow.parent = curve
            arrow.name =str(collector) + name + " body"
            
            #set arrow to curve
            curveLength = sum(s.calc_length() for s in curve.evaluated_get(bpy.context.evaluated_depsgraph_get()).data.splines)

            curveconst = bpy.context.window_manager.headroom * scale

            arrow.modifiers["Array"].fit_length = curveLength - curveconst
            arrow.modifiers["Curve"].object = curve

            #arrowtips
            mesh = bpy.data.meshes.new("TriPlane")
            tips = bpy.data.objects.new("Plane", mesh)

            bpy.context.collection.objects.link(tips)

            bm = bmesh.new()
            bm.from_object(tips, bpy.context.view_layer.depsgraph)

            s = scale * 1.5
            bm.verts.new((s,s,0))
            bm.verts.new((s,-s,0))
            bm.verts.new((0,0,0))
           
            bmesh.ops.contextual_create(bm, geom=bm.verts)

            bm.to_mesh(mesh)
            
            bpy.context.view_layer.objects.active = tips

            bpy.ops.object.modifier_add(type='CURVE')

            #set tips to curve
            tips.parent = arrow
            tips.modifiers["Curve"].object = curve
            tips.name = name + " tip"
            
            #modify arrow location
            arrow.location[0] += curveconst
            tips.location[0] -= scale * 2
            
            #material settings

            dclc.objects.link(arrow)
            dclc.objects.link(tips)
            
            #color the arrows
            mat = bpy.data.materials.new(name = str(name))
        
            arrow.data.materials.append(mat)
            tips.data.materials.append(mat)

            mat.use_nodes = True
            mat.node_tree.nodes["Principled BSDF"].inputs['Alpha'].default_value = opacity
            mat.node_tree.nodes["Principled BSDF"].inputs['Base Color'].default_value = (r, g, b, opacity)
            mat.node_tree.nodes["Principled BSDF"].inputs['Specular'].default_value = 0.0
            

            #new = mat.node_tree.nodes.new('ShaderNodeRGB')

            #mat.node_tree.nodes.remove(mat.node_tree.nodes.get('Principled BSDF'))

            #mat.node_tree.links.new(new.outputs[0], mat.node_tree.nodes.get('Material Output').inputs[0])
            
            mat.blend_method = 'BLEND'
            mat.shadow_method = 'NONE'
            
            
            #mat.node_tree.nodes['RGB'].outputs[0].default_value = (r, g, b, opacity)
            
            #end of loop

            bpy.context.scene.collection.objects.unlink(arrow)
            bpy.context.scene.collection.objects.unlink(tips)

            counter = counter + 1

def createCurve(name, crv, d, t):
    # create curve
    dx, dy, dz = d
    tx, ty, tz = t
                
    dist = math.sqrt((dx - tx)**2 + (dy - ty)**2)
           

    curveData = bpy.data.curves.new(name, type='CURVE')
    curveData.dimensions = '3D'
    curveData.resolution_u = 10
                
    line = curveData.splines.new('BEZIER')
                
    line.bezier_points.add(2)
                
    mx, my, mz = midpoint(dx, dy, dz, tx, ty, tz)
                
    mz = mz + zlift(bpy.context.window_manager.lift, dist)
                
    m1x, m1y, m1z = midpoint(dx, dy, dz, mx, my, mz)
    m2x, m2y, m2z = midpoint(tx, ty, tz, mx, my, mz)
               
    #point d            
    line.bezier_points[0].co = (dx, dy, dz)
    line.bezier_points[0].handle_left = (dx, dy, dz)
    line.bezier_points[0].handle_right = (m1x, m1y, m1z)    
                    
    #midpoint
    line.bezier_points[1].co = (mx, my, mz)
    line.bezier_points[1].handle_left = ( m1x, m1y, mz)
    line.bezier_points[1].handle_right = (m2x, m2y, mz)
                
    #point
    line.bezier_points[2].co = (tx, ty, tz)
    line.bezier_points[2].handle_left = (m2x, m2y, m2z)
    line.bezier_points[2].handle_right = (tx, ty, tz)
            
    curve = bpy.data.objects.new(name, curveData)

    # attach to scene
    crv.objects.link(curve)

    return curve