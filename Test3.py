# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 21:47:57 2020

@author: Aishwarya Patange
"""

import cv2
import os
import numpy as np
from timeit import default_timer as timer 

os.chdir(r'E:/Aishwarya/IPMV')

img = cv2.imread('SampleRG2.tif', 0)
img2 = cv2.imread('SampleRG1.png', 1)
conn = int(input('Enter Connectivity (4 / 8) :'))
threshold = int(input('Enter Threshold Value : '))

start = timer()

reg1 = region_growth(img, 173, 788, threshold, conn)
vect = timer() - start
#res = cv2.bitwise_and(img,img2,mask = mask)
cv2.imshow('Test', img)
cv2.imshow('Test2', reg1)

#cv2.imshow('Test3', img3)
print('Time Taken : %f', vect)
cv2.waitKey(0)
cv2.destroyAllWindows()



def region_growth(img, x, y, threshold=1, conn=4):
    
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

x, y =[], []    
for i in range(50):
    start = timer()
    reg1 = region_growth(img, 219, 118, i, 4)
    vect = timer() - start
    x.append(i)
    y.append(vect)
        
import matplotlib.pyplot as plt
plt.plot(y)
plt.ylabel('Time')
plt.xlabel('Threshold')
plt.show()
    