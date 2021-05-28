# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 19:10:33 2020

@author: Aishwarya Patange
"""

from tkinter import *
from PIL import Image, ImageTk
from tkinter import filedialog
from tkinter import ttk
import cv2
from math import ceil
import numpy as np
import os

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

class Window(Frame):
    img = None
    flaag1 = False
    file_name = None
    conn = None
    tentry = None 
    var1 = None
    x2 = None
    y2 = None
    seedButton = None
    dest_name = None
    def __init__(self, master = None):
        Frame.__init__(self, master)
        self.master = master
        
        self.pack(fill=BOTH, expand=1)
        
        #Menu Bar
        menu = Menu(self.master)
        self.master.config(menu = menu)        
        fileMenu = Menu(menu, tearoff=0)
        fileMenu.add_command(label="Exit", command=self.exitProgram)
        menu.add_cascade(label="File", menu=fileMenu)        
        helpMenu = Menu(menu, tearoff=0)
        helpMenu.add_command(label="Help")
        menu.add_cascade(label="Help", menu=helpMenu)
        
        ##Heading
        welcome1 = Label(self, text="Welcome To Image Segmentation", font = 'bold')
        welcome1.grid(row = 0, column = 1, sticky = W+E+N+S, padx = 10, pady=2, columnspan = 3)
        welcome2 = Label(self, text="Using Region Growing Algorithm", font = 'bold')
        welcome2.grid(row = 1, column = 1, sticky = W+E+N+S, padx = 10, pady=2, columnspan = 3)
        
        #Selection Label
        instrut = Label(self, text= 'Select Image File', borderwidth = 3, relief="ridge", width = 25)
        instrut.grid(row = 2, column = 1, sticky = N, padx = 10, pady=2)      
        
        #Selection Button
        fileButt = Button(self, text='Browse', command=self.open_file)
        fileButt.grid(row = 2, column = 3, sticky = N, padx = 10, pady=2)
        
        #Connectivity Selection
        conn_label = Label(self, text='Choose Connectivity', borderwidth = 3, relief="ridge", width = 25).grid(row = 4, column = 1, sticky = N, padx = 10, pady =2)
        self.conn = IntVar()
        self.conn.set(4)
        conn_drop = OptionMenu(self, self.conn, 4, 8).grid(row = 4, column = 2, sticky = N, padx = 10, pady =2)
        
        #Threshold Selection
        thresh_label = Label(self, text='Choose Threshold', borderwidth = 3, relief="ridge", width = 25).grid(row = 5, column = 1, sticky = N, padx = 10, pady =2)
        self.tentry = Entry(self, text='Enter Threshold', borderwidth=5)
        self.tentry.grid(row = 5, column = 2, sticky = N, padx = 10, pady =2)
        
        ##Select Seed Point Entry
        sel_label = Label(self, text='Seed Selection Method', borderwidth = 3, relief="ridge", width = 25).grid(row = 6, column = 1, sticky = N, padx = 10, pady =2)
        self.var1 = StringVar()
        R1 = Radiobutton(self , text="Manual", variable=self.var1, value='1', command=self.sel).grid(row = 6, column = 2, sticky = N, padx = 10, pady =2)
        R2 = Radiobutton(self , text="Using Mouse", variable=self.var1, value='2', command=self.sel).grid(row = 6, column = 3, sticky = N, padx = 10, pady =2)
        
        ##Manual Seed Selection
        man_label = Label(self, text='(x, y)', borderwidth = 3, relief="ridge", width = 25).grid(row = 7, column = 1, sticky = N, padx = 10, pady =2)
        self.x1 = Entry(self, text='x', borderwidth=5, state = 'disabled')
        self.x1.grid(row = 7, column = 2, sticky = N, padx = 10, pady =2)
        self.y1 = Entry(self, text='y', borderwidth=5, state = 'disabled')
        self.y1.grid(row = 7, column = 3, sticky = N, padx = 10, pady =2)
        
        ##Seed Selection Using Mouse
        self.seedButton = Button(self, text="Select Using Mouse", command=self.mouse_selection, state = 'disable')
        self.seedButton.grid(row = 8, column = 2, sticky = W+E+N+S, padx = 10, pady=2)
        
        #Destination
        instrut = Label(self, text= 'Select Destination Directory', borderwidth = 3, relief="ridge", width = 25)
        instrut.grid(row = 9, column = 1, sticky = N, padx = 10, pady=2)      
        
        #Destination Button
        fileButt = Button(self, text='Browse', command=self.open_file_dest)
        fileButt.grid(row = 9, column = 3, sticky = N, padx = 10, pady=2)
        
        ##Exit Button
        exitButton = Button(self, text="Exit", command=self.exitProgram)
        exitButton.grid(row = 10, column = 3, sticky = N, padx = 10, pady=2)
        
        ##Submit Button
        submitButton = Button(self, text="Submit", width = 25, command=self.submit)
        submitButton.grid(row = 10, column = 1, sticky = N, padx = 10, pady=2)
                
    def exitProgram(self):
        root.destroy()
    
    def sel(self):
        if self.var1.get() == "1":
            self.x1.configure(state = 'normal')
            self.y1.configure(state = 'normal')
            self.seedButton.configure(state = 'disable')
        elif self.var1.get() == '2':
            self.x1.configure(state = 'disable')
            self.y1.configure(state = 'disable')
            self.seedButton.configure(state = 'normal')
    
    def mouse_selection(self):
        gmi = getMouseInput(self.file_name)
        self.x2, self.y2 = gmi.getInput()
        mouseLabel = Label(self, text = '('+self.x2+', '+self.y2+')', borderwidth = 3, relief="ridge", width = 20).grid(row = 8, column = 3, sticky =  N, padx = 10, pady =2)
            
    def submit(self):
        if self.file_name == None:
            messagebox.showerror("Error", "Please Choose a File!")
        elif self.tentry.get() == "":
            messagebox.showerror("Error", "Please Enter Threshold!")
        elif (not(self.tentry.get().isdigit())):
            messagebox.showerror("Error", "Please Enter Numeric Threshold!")
        elif (self.var1.get() == '1') and ((self.x1.get() =='') or (self.y1.get() =='')):
            messagebox.showerror("Error", "Please Enter Seed Point (x, y)!")
        elif (self.var1.get()==''):
            messagebox.showerror("Error", "Choose Seed Selection Method!")
        elif (self.var1.get() == '1') and ((not(self.x1.get().isdigit())) or (not(self.y1.get().isdigit()))):
            messagebox.showerror("Error", "Please Enter Numeric Seed Point (x, y)!")
        elif (self.var1.get() == '1') and (self.x1.get().isdigit()) and (self.y1.get().isdigit()) and ((int(self.x1.get()) > cv2.imread(self.file_name, 1).shape[1]) or (int(self.y1.get()) > cv2.imread(self.file_name, 1).shape[0])):
            messagebox.showerror("Error", "Seed Points Out Of Bounds!")
        elif self.dest_name == None or self.dest_name == "":
            messagebox.showerror("Error", "Please Choose a Destination!")
        else:

            if self.var1.get() == '1':
                regionGrow1 = regionGrow()
                reg2 = regionGrow1.region_growth(self.file_name, int(self.y1.get()), int(self.x1.get()), self.dest_name, int(self.tentry.get()), int(self.conn.get()))
            elif self.var1.get() == '2':
                regionGrow1 = regionGrow()
                reg2 = regionGrow1.region_growth(self.file_name, int(self.y2), int(self.x2), self.dest_name, int(self.tentry.get()), int(self.conn.get()))
            messagebox.showinfo("Completed", "Completed!")
            """
            print("success")
            print(self.conn.get())
            print(self.file_name)
            print(self.tentry.get())
            print(self.var1.get())
            print(self.x1.get())
            print(self.y1.get())
            print(self.x2)
            print(self.y2)
            print(self.dest_name)
            cv2.imshow('Output', reg2)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            """
            base=os.path.basename(self.file_name)
            os.chdir(self.dest_name)
            cv2.imwrite('New_'+os.path.splitext(base)[0]+'.png', reg2)
    def helpMe(self):
        pass
    
    def open_file_dest(self):
        filename = filedialog.askdirectory(initialdir = 'C:/', title = 'Select Destination Folder')
        if filename!= None:
            filename_label = Label(self, text=filename, borderwidth = 3, relief="sunken",).grid(row = 9, column = 2, sticky = N, padx = 10, pady=2)
            self.dest_name = filename
            
    def open_file(self):
        if self.flaag1 == True:
            self.img.grid_forget()
        filename = filedialog.askopenfilename(initialdir = 'C:/', title = 'Select Image File', filetypes=(('All Files', '*.png *.jpg *.tif'), ('PNG Files', '*.png'), ('PNG Files', '*.png'),('JPG Files', '*.jpg'), ('TIFF Files', '*.tif')))
        if filename!= None:
            filename_label = Label(self, text=filename, borderwidth = 3, relief="sunken",).grid(row = 2, column = 2, sticky = N, padx = 10, pady=2)
            self.file_name = filename
            load = Image.open(filename)
            u, v = load.size
            rr = min(400/u, 300/v)
            resized = load.resize((ceil(u*rr), ceil(v*rr)), Image.ANTIALIAS)
            render = ImageTk.PhotoImage(resized)   
            self.img = Label(self, image=None)        
            self.img.grid_forget()
            self.img.configure(image=render)
            self.img.image = render
            self.img.grid(row = 3, column = 2, sticky = N, padx = 10, pady=2, columnspan=2)
            self.flaag1 = True
            
        
        
##Initialize
root = Tk()
app = Window(root)

##Specifications of the Window
root.wm_title('Region Growth')
root.geometry("")
root.iconbitmap(r'E:\Aishwarya\IPMV\IconBitmap.ico')
root.resizable(False, False)
root.mainloop()