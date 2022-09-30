#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ase import Atoms
from ase.io import write
from numpy import *  # NumPy
import os
from os import listdir
from os.path import isfile, join
from copy import deepcopy

import plot_wireframe
import wireframe_to_scad

working_directory_path=os.getcwd()        # Grab working directory path
os.system('rm *.pov')
os.system('rm *.ini')
os.system('rm *.png')

picture_size=500

def plot_stl(position, cell, filename):
    
    # Make STL file
    plot_wireframe.make_wireframe(position, cell)
    wireframe_to_scad.wireframetoscad('wireframe.obj', radius=0.2, nodesize=3.)
    os.system("openscad -o lattice.stl wireframe.scad") # This step takes a bit of time - generation of the stl by Openscad with CGAL library
    #os.system("mv wireframe.obj "+filename+".obj")

def plot_stl_blender(a):
    
    # Make STL file
    plot_wireframe.make_wireframe(a.positions, a.cell)
    os.system('blender --background --python blender_inflate.py')

def plot_image(a):
    
    k=0
    max_i=30
    
    for i in range(0, max_i):
        k+=1
        
        rot = str(6*i)+'x, '+str(3*i)+'y, '+str(3*i)+'z'  # found using ag: 'view -> rotate'
        
        kwargs = {
            'rotation'      : rot, # text string with rotation (default='' )
            'radii'         : 0.5, # float, or a list with one float per atom
            'colors'        : None,# List: one (r, g, b) tuple per atom
            'show_unit_cell': 2,   # 0, 1, or 2 to not show, show, and show all of cell
            }
        if k<10:
            str_img='00'+str(k)
        elif k<100:
            str_img='0'+str(k)
        else:
            str_img=str(k)
        write(str_img+'.png', a , **kwargs)
        
    png_files = [f for f in os.listdir(working_directory_path) if f.endswith('.png')]
    for i_png in range(0, len(png_files)):
        os.system('convert '+str(png_files[i_png])+' -background white -alpha remove -alpha off '+str(png_files[i_png]))
        os.system('convert '+str(png_files[i_png])+' -gravity center -extent '+str(picture_size)+'x'+str(picture_size)+'  '+str(png_files[i_png]))
    
    os.system('convert -resize '+str(picture_size)+'x'+str(picture_size)+' -delay 30 -loop 0 *.png output_image.gif')
    os.system('rm *.png')

def plot_xsf(position, cell, filename):
    
    a_vector=cell[0]
    b_vector=cell[1]
    c_vector=cell[2]
    positions_array=position
    outputFile = open(filename+'.xsf','w')
    outputFile.writelines('CRYSTAL\n')
    outputFile.writelines('PRIMVEC\n')
    outputFile.writelines('%s   %s   %s\n' % (a_vector[0], a_vector[1], a_vector[2])) # cell
    outputFile.writelines('%s   %s   %s\n' % (b_vector[0], b_vector[1], b_vector[2])) # cell
    outputFile.writelines('%s   %s   %s\n' % (c_vector[0], c_vector[1], c_vector[2])) # cell
    outputFile.writelines('PRIMCOORD\n')
    outputFile.writelines(str(position.shape[0])+' 1\n')
    atome_code=10
    for i_p in range(0, position.shape[0]):
        outputFile.writelines('%s   %s   %s   %s\n' % (atome_code, positions_array[i_p, 0], positions_array[i_p, 1], positions_array[i_p, 2]))
    outputFile.close()

def plot_animation(a):
    
    # Make 3D view
    
    k=0
    max_i=300
    
    for i in range(0, max_i):
        
        k+=1
        
        # View used to start ag, and find desired viewing angle
        #view(atoms)
        rot = str(0.6*i)+'x, '+str(0.3*i)+'y, '+str(0.3*i)+'z'  # found using ag: 'view -> rotate'
        
        # Common kwargs for eps, png, pov
        kwargs = {
            'rotation'      : rot, # text string with rotation (default='' )
            'radii'         : 0.5, # float, or a list with one float per atom
            'colors'        : None,# List: one (r, g, b) tuple per atom
            'show_unit_cell': 2,   # 0, 1, or 2 to not show, show, and show all of cell
            }
        
    #    # Extra kwargs only available for povray (All units in angstrom)
        kwargs.update({
            'run_povray'   : True, # Run povray or just write .pov + .ini files
            'display'      : False,# Display while rendering
    #        'pause'        : True, # Pause when done rendering (only if display)
            'transparent'  : False,# Transparent background
            'canvas_width' : picture_size, # Width of canvas in pixels
    #        'canvas_height': picture_size, # Height of canvas in pixels 
            'camera_dist'  : 1000.,  # Distance from camera to front atom
            'image_plane'  : 10., # Distance from front atom to image plane
            'camera_type'  : 'orthographic', # perspective, ultra_wide_angle, orthographic
    #        'point_lights' : [],             # [[loc1, color1], [loc2, color2],...]
    #        'area_light'   : [(2., 3., 40.), # location
    #                          'White',       # color
    #                          .7, .7, 3, 3], # width, height, Nlamps_x, Nlamps_y
            'background'   : 'White',        # color
    #        'textures'     : None, # Length of atoms list of texture names
            'celllinewidth': 0.05,  # Radius of the cylinders representing the cell
            })
        
        if k<10:
            str_img='00'+str(k)
        elif k<100:
            str_img='0'+str(k)
        else:
            str_img=str(k)
        write(str_img+'.pov', a , **kwargs)
    
    png_files = [f for f in os.listdir(working_directory_path) if f.endswith('.png')]
    for i_png in range(0, len(png_files)):
        os.system('convert '+str(png_files[i_png])+' -background white -alpha remove -alpha off '+str(png_files[i_png]))
        os.system('convert '+str(png_files[i_png])+' -gravity center -extent '+str(picture_size)+'x'+str(picture_size)+'  '+str(png_files[i_png]))
    
    os.system('convert -resize '+str(picture_size)+'x'+str(picture_size)+' -delay 3 -loop 0 *.png output_anim.gif')
    os.system('rm *.pov')
    os.system('rm *.ini')
    os.system('rm *.png')
