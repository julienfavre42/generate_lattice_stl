import bpy
import os

radius_beam=0.25

# Import wireframe
file_loc=os.getcwd() 
file_name='/wireframe.obj'
imported_object = bpy.ops.import_scene.obj(filepath=file_loc+file_name)

# Rotate
bpy.ops.transform.rotate(value=1.5708, axis=(1, 0, 0), constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)

# Make curve
bpy.ops.object.select_all(action='DESELECT')
o = bpy.data.objects['wireframe']
o.select = True
bpy.context.scene.objects.active = o
bpy.ops.object.convert(target='CURVE')

# Make inflation
bpy.ops.mesh.primitive_circle_add(radius=radius_beam, view_align=False, enter_editmode=False, location=(0, 0, 0), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
c = bpy.data.objects['Circle']
bpy.ops.object.select_all(action='DESELECT')
c = bpy.data.objects['Circle']
c.select = True
bpy.context.scene.objects.active = c
bpy.ops.object.convert(target='CURVE')

#bpy.ops.object.mode_set(mode='EDIT')
#bpy.ops.curve.subdivide()               # Refine the circle
#bpy.ops.object.mode_set(mode='OBJECT')

bpy.ops.object.select_all(action='DESELECT')
o = bpy.data.objects['wireframe']
o.select = True
bpy.context.scene.objects.active = o
bpy.ops.object.convert(target='CURVE')
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.curve.subdivide()       # Refine wireframe - repeat 3 to 5 times
bpy.ops.curve.subdivide()
bpy.ops.curve.subdivide()
bpy.ops.curve.subdivide()

bpy.context.object.data.fill_mode='FULL'
bpy.context.object.data.use_fill_deform=True
bpy.data.curves['wireframe'].bevel_object = c
bpy.context.object.data.bevel_resolution=8
#bpy.context.object.data.twist_smooth=10
bpy.context.object.data.splines[0].use_smooth=True

# Select the volume
bpy.ops.object.mode_set(mode='OBJECT')
bpy.ops.object.select_all(action='DESELECT')
o.select = True

fPath = str((file_loc + '/lattice_blender.stl'))
bpy.ops.export_mesh.stl(filepath=fPath)
