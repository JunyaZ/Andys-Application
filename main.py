# -*- coding: utf-8 -*-
"""
Created on Thu Dec 20 16:59:07 2018

@author: Junya
"""''
from tkinter import *
from tkinter.messagebox import *
from Gui import LoginPage
from Gui import DatabaseInterface


root = Tk()  
root.title('Manager Login')  
width = 500  
height =720
screenwidth = root.winfo_screenwidth()    
screenheight = root.winfo_screenheight()   
alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth-width)/2, (screenheight-height)/2)  
root.geometry(alignstr)    # align center

"""Start program."""
page1 = DatabaseInterface()
root.mainloop()
print(" Closed the connetion to the DB")
        