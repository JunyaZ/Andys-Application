
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 10:29:27 2019
@author: Junya
"""

from webbot import Browser
import pandas as pd
import glob
from datetime import date, timedelta
from io import StringIO
import os
import time
import datetime
from ftplib import FTP 
import io
ftp = FTP("lbug.mirus.com", "AndysCorp", "5r3TqM69")
Path=os.path.join(os.path.expanduser("~"), "Downloads\\")
out=os.path.join(os.path.expanduser("~"), "Desktop\\")
listcode=['AFC - North Central','AFC - Central','AFC - Southwest']
def downloading(web,i):
    web.click(classname='primary-nav__company-img' , tag='span') 
    web.click(listcode[i], tag='span') 
    web.click('Reports',tag='span')
    time.sleep(3)
    web.click("Custom Report",tag='span')
    time.sleep(3)
    web.click('Get Report')
    time.sleep(3)
    print(listcode[i] + "Downloaded")
def filtering(Path,i):
    file=glob.glob(Path+"*.csv")
    df=pd.read_csv(file[0])
    yesterday = (datetime.datetime.now() - timedelta(1)).strftime('%Y-%m-%d_%H%M%S')
    yesterDate=yesterday.split(sep="_")[0]
    df=df[df["Date"]==yesterDate]
    for f in file:
        os.remove(f)
    buffer=StringIO()
    df.to_csv(buffer,index=False)
    bio = io.BytesIO(str.encode(buffer.getvalue()))
    ftp.storbinary('STOR '+listcode[i]+"_"+yesterday+'.csv', bio)
def webcall():
    web = Browser(showWindow=True)
    web.go_to('https://app.7shifts.com/employers/') 
    web.type('info@eatandys.com' , into='Email')
    web.click('NEXT' , tag='span')
    web.type('cust4rd' , into='Password' , id='passwordFieldId') 
    web.click('Login' , tag='span')
    for i in range(0,len(listcode)):
        downloading(web,i)
        filtering(Path,i)
    web.quit() 
    
if __name__ == "__main__":
    webcall()

