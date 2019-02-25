# -*- coding: utf-8 -*-
"""
Created on Wed Feb 20 09:44:13 2019

@author: Junya
"""
import pandas as pd
import datetime
import numpy as np
import os
import glob
import shutil
from simpledbf import Dbf5
import math
df=pd.read_csv("dataout.csv")
#GroupFeatures=["HOUR","MINUTE"]
GroupFeatures=["HOUR"]
Choc_Modifier=df[(df["ITEM"]==10085) | (df["ITEM"]==2044) | (df["ITEM"]==10250)]
Custard_bar_count=df[df["ITEM"]==6110].ITEM.count()/6
df= df[df["OUNCE"].notnull()]
Modifed_Ratio = (Choc_Modifier.ITEM.count()-Custard_bar_count)/df.ITEM.count()
print("number of Choc_Modifier:",Choc_Modifier.ITEM.count(),"number of Custard bar ( Chocolate only):",Custard_bar_count)
print("The Modifed Ratio is:",Modifed_Ratio*100,"%" ) 

#===================================#
GROUP=df.groupby(["DOB","WEEKDAY","CUSTARD_TYPE","HOUR"])["OUNCES"].sum().reset_index()
counter=GROUP.groupby(["HOUR","CUSTARD_TYPE"])["DOB"].count().reset_index().rename(columns={'DOB':'Day_counter'})
#===================================#
ounces=df.groupby(["DOB","WEEKDAY","CUSTARD_TYPE"]+GroupFeatures)["OUNCES"].sum().reset_index()
treats=df.groupby(["DOB","WEEKDAY","CUSTARD_TYPE"]+GroupFeatures)["QUANTITY"].sum().reset_index()
a=treats.groupby(["CUSTARD_TYPE"]+GroupFeatures)["QUANTITY"].sum().reset_index()
b=ounces.groupby(["CUSTARD_TYPE"]+GroupFeatures)["OUNCES"].sum().reset_index()

#===================================#
a=pd.merge(a,counter, on=['HOUR','CUSTARD_TYPE'], how='left')
b=pd.merge(b,counter, on=['HOUR','CUSTARD_TYPE'], how='left')
a['QUANTITY'] = a['QUANTITY']/a['Day_counter']
b['OUNCES'] = b['OUNCES']/b['Day_counter']
#===================================#

Output =pd.merge(a,b, on=(["CUSTARD_TYPE"]+GroupFeatures), how='left', indicator=True)
chocolate = Output.groupby(['CUSTARD_TYPE']).get_group('chocolate').rename(columns={'CUSTARD_TYPE':'Chocolate',"QUANTITY":"Treats_C","OUNCES":"OUNCES_C"})
vanilla= Output.groupby(['CUSTARD_TYPE']).get_group('vanilla').rename(columns={'CUSTARD_TYPE':'Vanilla',"QUANTITY":"Treats_V","OUNCES":"OUNCES_V"})
chocolate["Treats_C"] = chocolate.apply(lambda row : row["Treats_C"]*(1+Modifed_Ratio),axis=1)
chocolate["OUNCES_C"] = chocolate.apply(lambda row : row["OUNCES_C"]*(1+Modifed_Ratio),axis=1)
vanilla["OUNCES_V"] = vanilla.apply(lambda row : row["OUNCES_V"]*(1-Modifed_Ratio),axis=1)
vanilla["Treats_V"] = vanilla.apply(lambda row : row["Treats_V"]*(1-Modifed_Ratio),axis=1)
Mixresult= pd.merge(vanilla,chocolate, on=GroupFeatures, how='left')
Mixresult["Buckets_V"] = Mixresult.apply(lambda row : row["OUNCES_V"]/(128*3),axis=1)
Mixresult["Buckets_C"] = Mixresult.apply(lambda row : row["OUNCES_C"]/(128*3),axis=1)
Mix = Mixresult[GroupFeatures+['Treats_V', 'OUNCES_V','Buckets_V','Treats_C', 'OUNCES_C','Buckets_C']]
print("MIX",Mix)