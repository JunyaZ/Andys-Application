# -*- coding: utf-8 -*-
"""
Created on Fri Nov 16 16:26:20 2018

@author: Junya
"""
import os
import sys
from PIL import Image
import glob
from pathlib import Path
import PIL
import numpy as np

full_path =Path.cwd()
obspath, filename = os.path.split(full_path)

graphpath1= obspath + "\\Graphs\\Percentage_byCategory\\"
graphpath2= obspath + "\\Graphs\\Percentage_byHour\\"
graphpath3= obspath + "\\Graphs\\Precentage_byDay\\"
graphpath4= obspath + "\\Graphs\\TotalSales\\CategoryTotalSales\\"
graphpath5= obspath + "\\Graphs\\TotalSales\\TotalSalesPerMonth\\"
graphpath6= obspath + "\\Graphs\\TotalSales\\Trends\\"
testpath = obspath + "\\Graphs\\"

WEEKDAY= {0: "Sunday",1: "Monday", 2:"Tuesday",3: "Wednesday",
      4: "Thursday",5: "Friday",6: "Saturday"}        

globbed = glob.glob(testpath+ "*.png")

def Combined1(globbed):
    for i in range(len(WEEKDAY)):
        list_im = list(filter(lambda x: x.__contains__(WEEKDAY[i]), globbed))
        imgs    = [ PIL.Image.open(i) for i in list_im ]
        # pick the image which is the smallest, and resize the others to match it (can be arbitrary image shape here)
        min_shape = sorted( [(np.sum(i.size), i.size ) for i in imgs])[0][1]
        imgs_comb = np.hstack( (np.asarray( i.resize(min_shape) ) for i in imgs ) )
        
        # save that beautiful picture
#        imgs_comb = PIL.Image.fromarray( imgs_comb)
#        imgs_comb.save(WEEKDAY[i] +'_Combined.png' )    
        
        # for a vertical stacking it is simple: use vstack
        imgs_comb = np.vstack( (np.asarray( i.resize(min_shape) ) for i in imgs ) )
        imgs_comb = PIL.Image.fromarray( imgs_comb)
        imgs_comb.save(testpath+"Combined\\"+ WEEKDAY[i] +'_Combined.png' )
def Combined2(globbed):
    for i in range(0,len(globbed),7):
        list_im = globbed[i:i+7]
        imgs   = [ PIL.Image.open(i) for i in list_im ]
        # pick the image which is the smallest, and resize the others to match it (can be arbitrary image shape here)
        min_shape = sorted( [(np.sum(i.size), i.size ) for i in imgs])[0][1]
        imgs_comb = np.hstack( (np.asarray( i.resize(min_shape) ) for i in imgs ) )
        
        # save that beautiful picture
        imgs_comb = PIL.Image.fromarray( imgs_comb)
        imgs_comb.save(str(i)+ '_CombinedWEEK.png')    
        
        # for a vertical stacking it is simple: use vstack
#        imgs_comb = np.vstack( (np.asarray( i.resize(min_shape) ) for i in imgs ) )
#        imgs_comb = PIL.Image.fromarray( imgs_comb)
        imgs_comb.save(testpath+"Combined\\"+"Week_"+ str(int((i/7)+1)) + '_Combined.png')   
#Combined1(globbed)
Combined2(globbed)
