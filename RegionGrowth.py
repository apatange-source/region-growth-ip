# -*- coding: utf-8 -*-
"""
Created on Sun Apr  5 05:10:49 2020

@author: Aishwarya Patange
"""

import cv2
import numpy as np
import os

class regionGrow:   
    
    def __init__(self):
        pass
        
    def region_growth(self, filename, x, y, destination, threshold=1, conn=4):
        img = cv2.imread(filename,0)
        #Check Required Connectivity
        if conn == 4:
            orient = [(1, 0), (0, 1), (-1, 0), (0, -1)] #4 Connectivity
        elif conn == 8:
            orient = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)] #8 Connectivity
        else:
            print("Unknown Connectivity")
        
        #Dimensions of the unknown image
        dims = img.shape
    
        #Image to be returned
        reg = np.zeros((dims[0], dims[1]))
    
        #Seed Point Value
        mean_reg = float(img[x, y])
    
        size = 1
        pix_area = dims[0]*dims[1]
        
        #Cursor Pixel 
        cur_pix = [x, y]
    
        size = 1
    
        contour = [] # will be [ [[x1, y1], val1],..., [[xn, yn], valn] ]
        contour_val = []
        dist = 0 
    
        #Speading 
        while(dist<threshold and size<pix_area):
            #Adding Pixels
            for j in range(len(orient)):
                
                #Select New Candidate
                temp_pix = [cur_pix[0]+orient[j][0], cur_pix[1] + orient[j][1]]
            
                #Check if it belongs to the image
                is_in_img = dims[0]>temp_pix[0]>0 and dims[1]>temp_pix[1]>0 #Returns Boolean
            
                #Candidate is taken if not already selected
                if (is_in_img and (reg[temp_pix[0], temp_pix[1]] == 0)):
                    contour.append(temp_pix)
                    contour_val.append(img[temp_pix[0], temp_pix[1]])
                    reg[temp_pix[0], temp_pix[1]] = 150
        
            #Add the nearest pixel of the contour in it
            dist_list = [abs(i-mean_reg) for i in contour_val]
            dist = min(dist_list) #Get the minimum distance
            print(dist)
            index = dist_list.index(min(dist_list)) #Index of the minimum distance
            size+=1 #updating region size
            reg[cur_pix[0], cur_pix[1]] = 255
            
            #Updating mean must be float
            mean_reg = (mean_reg*size + float(contour_val[index]))/(size+1)
            
            #Updating Seed
            cur_pix = contour[index]

            #removing pixel from neighborhood
            del contour[index]
            del contour_val[index]

        return reg