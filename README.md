# Path-Tracer

To install, use the Blender's Prefrences>Addons>Install from file, and use Path-Tracer.zip from dling this repo.

Path Tracer is setup to read files in two forms, .txt or .csv. It reads from the directory that the blender file is saved to, so I reccommend saving your projects to their own directory. The example file format is show below:

.csv config{
TRNS,-80/-14/-2,-107/-27/-2,-99/-27/-2
-78/-9/-2,1,2,3
-78/-17/-2,4,5,6
-87/-14/-2,7,8,9
}

.txt config {
Ds
(23/15/27)
(16/-0/27)
(38/-1/27)

Ts
(-78/-9/-2)
(-78/-17/-2)
(-87/-14/-2)

Transmission
1
2
3
4
5
6
7
8
9
}

The breakpoints and color values are editable to create different scales. Other features include support for loading 3d models, 3d scans, of buildings, while removing the roof. Furthermore, there is the ability to non destructtively convert these models to B&W.
