# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 10:29:27 2019

@author: Junya
"""

from webbot import Browser
import pandas as pd
import glob
from datetime import date, timedelta
import os
import time
import datetime
Path=os.path.join(os.path.expanduser("~"), "Downloads\\")
out=os.path.join(os.path.expanduser("~"), "Desktop\\")
listcode=['AFC - North Central','AFC - Central','AFC - Southwest']
def downloading(web,i):
    web.click(classname='primary-nav__company-img' , tag='span') 
    web.click(listcode[i], tag='span') 
    web.click('Reports',tag='span')
    web.click('Custom Report',tag='span')
    time.sleep(2)
    web.click('Get Report',tag="button")
    time.sleep(3)
  
def filtering(Path,i):
    file=glob.glob(Path+"*.csv")
    df=pd.read_csv(file[0])
    print(df)
    yesterday = (datetime.datetime.now() - timedelta(1)).strftime('%m/%d/%Y_%H%M%S')
    df=df[df["Date"]==yesterday]
    for f in file:
        os.remove(f)
    print("File Removed!")
    day=datetime.datetime.strptime(yesterday, '%m/%d/%Y_%H%M%S').strftime("%Y-%m-%d")
    df.to_csv(out+listcode[i]+day+".csv",index=False)

def callweb():
    web = Browser()
    web.go_to('https://app.7shifts.com/employers/') 
    web.type('info@eatandys.com' , into='Email')
    web.click('NEXT' , tag='span')
    web.type('cust4rd' , into='Password' , id='passwordFieldId') 
    web.click('Login' , tag='span')   
    for i in range(0,len(listcode)): 
        downloading(web,i)
        filtering(Path,i)
    web.quit() 
callweb()
