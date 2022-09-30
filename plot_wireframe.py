# -*- coding: utf-8 -*-

# Import libraries
import math
from numpy import *
import numpy as np
from os import listdir
from os.path import isfile, join
import pandas as pd

def make_wireframe(nodes_array, cell_vectors):
    
    # Filter the duplicate nodes
    duplicate_threshold=1E-3
    pursue_index=1
    i=0
    while pursue_index==1:			# i-th point
        distance=sqrt(np.power((nodes_array[:,0]-nodes_array[i,0]),2)+np.power((nodes_array[:,1]-nodes_array[i,1]),2)+np.power((nodes_array[:,2]-nodes_array[i,2]),2))
        distance[i]=Inf
        min_dist_loc=min(distance)
        if min_dist_loc<duplicate_threshold:
            nodes_array=np.delete(nodes_array, [i], axis=0)
        i+=1
        if i<nodes_array.shape[0]:
            pursue_index=1
        else:
            pursue_index=0
    
    nodes_range=linspace(0,nodes_array.shape[0]-1, nodes_array.shape[0])
    
    # Calculate mindistance
    mindistance=Inf
    for i in range (0,nodes_array.shape[0]):			# i-th point
        distance=sqrt(np.power((nodes_array[:,0]-nodes_array[i,0]),2)+np.power((nodes_array[:,1]-nodes_array[i,1]),2)+np.power((nodes_array[:,2]-nodes_array[i,2]),2))
        min_dist_loc=min(distance[distance>1E-3])
        if mindistance>min_dist_loc:
            mindistance=min_dist_loc
    
    # Create the Connexion Array
    l_tol=1E-3*mindistance
    connexionarray=array([[0,0]])			# Array listing the different points pairs connected to form the network
    for i in range (0,nodes_array.shape[0]):			# i-th point
        distance=sqrt(np.power((nodes_array[:,0]-nodes_array[i,0]),2)+np.power((nodes_array[:,1]-nodes_array[i,1]),2)+np.power((nodes_array[:,2]-nodes_array[i,2]),2))
        potential_connexions_boolean=abs(distance-mindistance)<=l_tol
        potential_connexions=nodes_range[potential_connexions_boolean].astype(int)
        for j in range(0, potential_connexions.shape[0]):
            connexionarray=concatenate((connexionarray, array([[i+1,potential_connexions[j]+1]])), axis=0)
    
    # Clean up the connexion array to remove duplication
    deletelist=False*ones(connexionarray.shape[0])
    for i in range (0,connexionarray.shape[0]):
        thatisaduplicate=False*ones(connexionarray.shape[0])
        thatisaduplicate=(((connexionarray[i,0]==connexionarray[:,0])*(connexionarray[i,1]==connexionarray[:,1]))+((connexionarray[i,1]==connexionarray[:,0])*(connexionarray[i,0]==connexionarray[:,1])))
        thatisaduplicate[i]=False
        if deletelist[i]==0:
            deletelist+=thatisaduplicate
    
    connexionarray=connexionarray[deletelist==0]        
    connexionarray=np.delete(connexionarray, [0], axis=0)    # Remove the first line
    
    # Export data
    outputFile = open("wireframe.obj", 'w')
    for i in range (0, nodes_array.shape[0]):
        outputFile.writelines('v %s %s %s\n' % (nodes_array[i,0], nodes_array[i,1], nodes_array[i,2]))
    for i in range (0, connexionarray.shape[0]):
        outputFile.writelines('l %s %s \n' % (connexionarray[i,0], connexionarray[i,1]))
    outputFile.close()
    
    ############
    # Make cell
    
    nodes_array=np.zeros((8,3))
    nodes_array[1]=cell_vectors[0]
    nodes_array[2]=cell_vectors[1]
    nodes_array[3]=cell_vectors[2]
    nodes_array[4]=cell_vectors[0]+cell_vectors[1]
    nodes_array[5]=cell_vectors[1]+cell_vectors[2]
    nodes_array[6]=cell_vectors[0]+cell_vectors[2]
    nodes_array[7]=cell_vectors[0]+cell_vectors[1]+cell_vectors[2]
    connexionarray=np.array([[1,2], [1,3], [1,4], [2,3], [3,4], [2,4], [2,5], [2,7], [3,6], [3,5], [4,7], [4,6], [5,6], [6,7], [5,7], [5,8], [6,8], [7,8]])    
    outputFile = open("cell.obj", 'w')
    for i in range (0, nodes_array.shape[0]):
        outputFile.writelines('v %s %s %s\n' % (nodes_array[i,0], nodes_array[i,1], nodes_array[i,2]))
    for i in range (0, connexionarray.shape[0]):
        outputFile.writelines('l %s %s \n' % (connexionarray[i,0], connexionarray[i,1]))
    outputFile.close()