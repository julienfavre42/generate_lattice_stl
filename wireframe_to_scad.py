import math
from numpy import *
import numpy as np
import os
from os import listdir
from os.path import isfile, join
import pandas as pd


def wireframetoscad(filename, radius, nodesize):
    
    data = pd.read_csv(filename, sep=" ", header=None)
    data.columns = ["type", "x", "y", "z"]
    nodes=data[data["type"]=="v"]
    lines=data[data["type"]=="l"]
    lines_copy=lines.copy()
    lines_copy.drop_duplicates(subset=None, keep = False, inplace = True)
    connexionarray=np.asarray(lines_copy.values.tolist())
    ver=np.asarray(nodes.values.tolist())
    
    connexionarray=np.delete(connexionarray, 0, 1)
    connexionarray=np.delete(connexionarray, 2, 1)
    connexionarray=connexionarray.astype(np.float)
    ver=np.delete(ver, 0, 1)
    ver=ver.astype(np.float)
    connexionarray=connexionarray-1
    
    mindistance=Inf
    for i in range (0,ver.shape[0]):			# i-th point
        distance=sqrt(np.power((ver[:,0]-ver[i,0]),2)+np.power((ver[:,1]-ver[i,1]),2)+np.power((ver[:,2]-ver[i,2]),2))
        min_dist_loc=min(distance[distance>1E-3])
        if mindistance>min_dist_loc:
            mindistance=min_dist_loc
    
    # Compute translation and rotation elements
    
    rotationarray=array([[0,0,0,0]]);
    translationarray=array([[0,0,0]]);
    positionvectarray=array([[0,0,0]]);
    for i in range (0,connexionarray.shape[0]):
    	if (sqrt(pow(ver[int(connexionarray[i,0]),0],2)+pow(ver[int(connexionarray[i,0]),1],2)+pow(ver[int(connexionarray[i,0]),2],2)))<=(sqrt(pow(ver[int(connexionarray[i,1]),0],2)+pow(ver[int(connexionarray[i,1]),1],2)+pow(ver[int(connexionarray[i,1]),2],2))):
    		point1=array([[ver[int(connexionarray[i,0]),0], ver[int(connexionarray[i,0]),1], ver[int(connexionarray[i,0]),2]]])
    		point2=array([[ver[int(connexionarray[i,1]),0], ver[int(connexionarray[i,1]),1], ver[int(connexionarray[i,1]),2]]])
    	else:
    		point1=array([[ver[int(connexionarray[i,1]),0], ver[int(connexionarray[i,1]),1], ver[int(connexionarray[i,1]),2]]])
    		point2=array([[ver[int(connexionarray[i,0]),0], ver[int(connexionarray[i,0]),1], ver[int(connexionarray[i,0]),2]]])    # Classify the two points of the beam in a specific order : the 1 is closer from the origin than the 2
    	positionvect=array([[(point2[0,0]-point1[0,0]),(point2[0,1]-point1[0,1]),(point2[0,2]-point1[0,2])]])       # Vector along the beam
    	for ir in range (0, positionvect.shape[1]):        
    		if (abs(positionvect[0,ir])<=1E-9):
    			positionvect[0,ir]=0
    	positionvectornorm=sqrt(pow(positionvect[0,0],2)+pow(positionvect[0,1],2)+pow(positionvect[0,2],2))       # Norm of the position vector
    	if positionvectornorm>0 and (pow(positionvect[0,1],2)+pow(positionvect[0,2],2))>0:
    		anglegamma=(180/pi)*arcsin(sqrt(pow(positionvect[0,1],2)+pow(positionvect[0,2],2))/positionvectornorm)
    		if positionvect[0,0]<0:
    			anglegamma=180-anglegamma
    		rotvector=array([[0,-(positionvect[0,2]/sqrt(pow(positionvect[0,1],2)+pow(positionvect[0,2],2))),(positionvect[0,1]/sqrt(pow(positionvect[0,1],2)+pow(positionvect[0,2],2)))]])
    		if abs(rotvector[0,0])<1E-6:
    			rotvector[0,0]=0
    		if abs(rotvector[0,1])<1E-6:
    			rotvector[0,1]=0
    		if abs(rotvector[0,2])<1E-6:
    			rotvector[0,2]=0
    	else:
    		anglegamma=0
    		rotvect=array([[1,0,0]])
    	if abs(anglegamma)<1E-6:
    		anglegamma=0
    	rotelement=array([[rotvector[0,0], rotvector[0,1],rotvector[0,2],anglegamma]])
    	rotationarray=concatenate((rotationarray, rotelement), axis=0)
    	translatex=0.5*(point1[0,0]+point2[0,0])
    	translatey=0.5*(point1[0,1]+point2[0,1])
    	translatez=0.5*(point1[0,2]+point2[0,2])
    	transelement=array([[translatex, translatey,translatez]])
    	translationarray=concatenate((translationarray, transelement), axis=0)
    	positionvectelement=array([[positionvect[0,0], positionvect[0,1],positionvect[0,2]]])
    	positionvectarray=concatenate((positionvectarray, positionvectelement), axis=0)
    
    
    # WRITE  FILE
    
    outputFile = open(filename.replace('.obj', '')+'.scad','w')
    
    # Write parameters matrix
    outputFile.writelines('array = [ \n')
    for i in range(1, translationarray.shape[0]):
    	if i==translationarray.shape[0]-1:
    		outputFile.writelines('[%s, %s, %s, %s,  %s,  %s, %s, %s, %s]\n' % (translationarray[i,0], translationarray[i,1], translationarray[i,2], rotationarray[i,1], rotationarray[i,2], rotationarray[i,3], positionvectarray[i,0], positionvectarray[i,1], positionvectarray[i,2]))
    	else:
    		outputFile.writelines('[%s, %s, %s, %s,  %s,  %s, %s, %s, %s],\n' % (translationarray[i,0], translationarray[i,1], translationarray[i,2], rotationarray[i,1], rotationarray[i,2], rotationarray[i,3], positionvectarray[i,0], positionvectarray[i,1], positionvectarray[i,2]))
    outputFile.writelines('    ];\n')
    
    # Write scad script
    outputFile.writelines('radius=%s; \n' % (radius))
    outputFile.writelines('nodesize=%s; \n' % (nodesize))
    outputFile.writelines('mindistance=%s; \n' % (mindistance))
    
    outputFile.writelines('\n')
    outputFile.writelines('for (i = [ 0 : (len(array)-1)] ) {\n')
    outputFile.writelines('union () {\n')
    outputFile.writelines('translate([array[i][0], array[i][1], array[i][2]])  rotate(a=array[i][5], v=[0, array[i][3], array[i][4]]) rotate(a=90, v=[0, 1, 0]) union () ')
    outputFile.writelines('{ cylinder(h=mindistance,r=radius,center=true,$fn=15); translate([0,0,mindistance*0.5]) sphere(r=radius*nodesize, center=true, $fn=15);')
    outputFile.writelines('translate([0,0,-mindistance*0.5]) sphere(r=radius*nodesize, center=true, $fn=15);\n')
    outputFile.writelines('}\n')
    outputFile.writelines('}\n')
    outputFile.writelines('}\n')
    outputFile.close()