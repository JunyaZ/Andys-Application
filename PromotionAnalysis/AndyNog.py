# -*- coding: utf-8 -*-
"""
Created on Mon Jan 14 09:10:15 2019

@author: Junya
"""
import pandas as pd
import xlrd
from pathlib import Path
import os
import glob

DatesName ={
"2017_1016_1022": "10/16-10/22/2017",
"2017_1023_1029" : "10/23-10/29/2017",
"2017_1030_1101" : "10/30-11/01/2017",
"2017_1102_1105" :"11/02-11/05/2017",
"2017_1106_1112" :"11/06-11/12/2017",
"2017_1113_1119" :"11/13-11/19/2017",
"2017_1120_1126" :"11/20-11/26/2017",
"2017_1127_1203" :"11/27-12/03/2017",
"2017_1204_1210" :"12/04-12/10/2017",
"2017_1211_1217" :"12/11-12/17/2017",
"2017_1218_1224" :"12/18-12/24/2017",
"2017_1225_1231" :"12/25-12/31/2017",



"2018_1015_1021" :"10/15-10/21/2018",
"2018_1022_1028" :"10/22-10/28/2018",
"2018_1029_1031" :"10/29-10/31/2018",
"2018_1101_1104" :"11/01-11/04/2018",
"2018_1105_1111" :"11/05-11/11/2018",
"2018_1112_1118" :"11/12-11/18/2018",
"2018_1119_1125" :"11/19-11/25/2018",
"2018_1126_1202" :"11/26-12/02/2018",
"2018_1203_1209" :"12/03-12/09/2018",
"2018_1210_1216" :"12/10-12/16/2018",
"2018_1217_1223" :"12/17-12/23/2018",
"2018_1224_1230" :"12/24-12/30/2018"

}        
obspath, filename = os.path.split(Path.cwd())
path2018 = obspath + "\\AndynogPeppermint\\2018\\"
path2017 = obspath + "\\AndynogPeppermint\\2017\\"
output = obspath + "\\AndynogPeppermint\\"
globbed2018 = glob.glob(path2018+"*.xls")
globbed2017 =glob.glob(path2017+"*.xls")

def Calculation(globbedfile):
    PEPPER=pd.DataFrame()
    ANDY=pd.DataFrame()
    for file in globbedfile:
        wb = xlrd.open_workbook(file, logfile=open(os.devnull, 'w'))
        df= pd.read_excel(wb,index=False,skiprows=6,engine='xlrd')
        df=df.rename(index=str, columns={"Unnamed: 1": "Name"})
        df=df.set_index(df.Name)
        df =df[df["Unnamed: 0"]!="ID"]
        df =df[df["Unnamed: 0"]!=10035]
        df =df[df["Name"].notnull()]
        df = df[df.columns[~df.columns.str.contains('Unnamed:')]]
        Total = df.sum().rename("TotalSales")
        Peppermint = df[df["Name"].str.contains("Peppermint", na=False)].T
        AndyNog = df[df["Name"].str.contains("Andy Nog", na=False)].T
        Peppermint = Peppermint.rename(columns={"Peppermint": file.split(sep="\\")[-1].split(sep=".")[0]})
        AndyNog = AndyNog.rename(columns={"Lg Andy Nog": file.split(sep="\\")[-1].split(sep=".")[0],"Andy Nog": file.split(sep="\\")[-1].split(sep=".")[0]})
        PEPPER= pd.concat([PEPPER,Peppermint,Total],axis=1)
        ANDY= pd.concat([ANDY,AndyNog,Total],axis=1)
        PEPPER =PEPPER.rename(columns=DatesName)
        ANDY =ANDY.rename(columns=DatesName)   
    return PEPPER,ANDY

peppermint2018,andy2018 = Calculation(globbed2018)
peppermint2017,andy2017 = Calculation(globbed2017)


peppermint2018= pd.concat([peppermint2017,peppermint2018],axis=1)
andy2018= pd.concat([andy2017,andy2018],axis=1)

writer = pd.ExcelWriter(output + "AndyNog.xls")
peppermint2018.to_excel(writer,"peppermint2018")
andy2018.to_excel(writer,"andynog2018")
writer.save()

