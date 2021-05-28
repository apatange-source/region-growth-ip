# -*- coding: utf-8 -*-
"""
Created on Sun Mar 15 17:40:03 2020

@author: Aishwarya Patange
"""
import numpy as np
import cv2
import os



a = cv2.imread(r'E:\Aishwarya\IPMV\SampleRG2.tif', 1)

def draw_circle(event, x, y, flags, params):
    global mouseX, mouseY
    if event == cv2.EVENT_LBUTTONDBLCLK:
        cv2.circle(a, (x, y), 3, (255, 0, 0), -1)
        mouseX, mouseY = x, y
        
cv2.namedWindow('Image')
cv2.setMouseCallback('Image', draw_circle)


while (1):
    cv2.imshow('Image', a)
    k = cv2.waitKey(10) & 0xFF
    if k == 27:
        cv2.destroyAllWindows()
        break
    elif k == ord('a'):
        print(mouseX, mouseY)

    