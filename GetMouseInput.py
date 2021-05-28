# -*- coding: utf-8 -*-
"""
Created on Sun Apr  5 03:07:33 2020

@author: Aishwarya Patange
"""

import cv2

class getMouseInput:
    mouseX = None
    mouseY = None
    img = None
    fla = None
    def __init__(self, filepath):
        self.mouseX = None
        self.mouseY = None
        self.img = cv2.imread(filepath, 1)
        self.fla = True
    def draw_circle(self, event, x, y, flags, params):
        if event == cv2.EVENT_LBUTTONDBLCLK:
            cv2.circle(self.img, (x, y), 3, (255, 0, 0), -1)
            self.mouseX, self.mouseY = x, y
            self.fla = False
    def getInput(self):
        winname = 'Double Click to Select'
        cv2.namedWindow(winname)
        cv2.setMouseCallback(winname, self.draw_circle)                
        while 1:
            cv2.imshow(winname, self.img)
            k = cv2.waitKey(10) & 0xFF
            if k == 27:
                cv2.destroyAllWindows()
                break
            if self.fla==False:
                cv2.destroyAllWindows()
                break
        return str(self.mouseX), str(self.mouseY)


    
    
    
