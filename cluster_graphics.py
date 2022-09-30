from ase import Atoms
from ase.io import write
from ase.optimize import QuasiNewton
from ase.eos import EquationOfState
from ase.io import read
#from gpaw import GPAW, PW, FermiDirac
import string
import fileinput
from copy import deepcopy
from numpy import *  # NumPy
import numpy as np
from math import *
import os
import pandas as pd
from os import listdir
from os.path import isfile, join
from matplotlib import *
import matplotlib.pyplot as plt

import plot_cluster

seed_base='Fe'

# Crystal definition
a_param=3.5
repetition_number=3


a0 = a_param
#a = Atoms(symbols=seed_base, pbc=True, cell=[[0.0, a0/2., a0/2.], [a0/2., 0.0, a0/2.], [a0/2., a0/2., 0.0]])   # FCC rhombohedron

# FCC
a= Atoms(seed_base+str(14), [(0, 0, 0), (0, a0/2., a0/2.), (a0/2., a0/2., 0), (a0/2., 0, a0/2.), (a0, a0/2., a0/2.), (a0/2., a0/2., a0), (a0/2., a0, a0/2.), (a0, 0, 0), (0, a0, 0), (0, 0, a0), (a0, a0, 0), (0, a0, a0), (a0, 0, a0), (a0, a0, a0)], cell=[[a0, 0.0, 0.0], [0.0, a0, 0.0], [0.0, 0.0, a0]], pbc=True)   # FCC cube

# BCC
#a= Atoms(seed_base+str(9), [(0, 0, 0), (a0/2., a0/2., a0/2.), (a0, 0, 0), (0, a0, 0), (0, 0, a0), (a0, a0, 0), (0, a0, a0), (a0, 0, a0), (a0, a0, a0)], cell=[[a0, 0.0, 0.0], [0.0, a0, 0.0], [0.0, 0.0, a0]], pbc=True)   # FCC cube

a=a*(repetition_number,repetition_number,repetition_number)
a.center()

a.cell0=deepcopy(a.cell)
a.positions0=deepcopy(a.positions)

# Plot the cell
plot_cluster.plot_stl(a.positions, a.cell, "crystal") # Command to make a scad file and then a stl file from Openscad (can be time consuming to run...)
plot_cluster.plot_xsf(a.positions, a.cell, "crystal") # Command to generate a xsf file for XcrysDen
plot_cluster.plot_stl_blender(a) # Command to generate a stl from Blender
plot_cluster.plot_image(a)      # Command to plot images and a gif from ASE
plot_cluster.plot_animation(a) # Command to plot images and a gif from ASE - with 3D rendering using Povray

print('end')
