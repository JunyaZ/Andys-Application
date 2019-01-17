# -*- coding: utf-8 -*-
"""
Created on Wed Nov 21 09:49:56 2018

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

filted_columns_name = ['ITEM','ITEM_NAME','ITEM_SIZE','CATEGORY_NAME','PRICE','HOUR',
   'MINUTE','DOB','QUANTITY','DISCPRIC','OUNCE','CUSTARD_TYPE']

currentpath = os.getcwd()
output =currentpath+"\\Output"
datapath, folder = os.path.split(currentpath)

def SelectDate(inputDate):
    for i in range(1,7):
        week_ago = inputDate - datetime.timedelta(days=(7*i))
        week_ago = week_ago.strftime("%Y%m%d")
        for path, subdirs, files in os.walk(datapath+"\\"+ week_ago):
            for name in files:
                if name == "GNDITEM.Dbf":    
                    filename = os.path.join(path, name)
                    shutil.copy(filename,os.path.join(output, "GNDITEM" + os.path.split(path)[1] + ".Dbf"))

#--------------------preprocessing----------------------------------#
def preprocessing():
    globbed_file = glob.glob(output+"\\"+"*.Dbf")
    counter=0
    Item_Category= pd.read_csv(os.getcwd()+"\\item.csv")
    Combine =pd.DataFrame()
    for file in globbed_file:
        Table = Dbf5(file)
        df=Table.to_dataframe()
        counter+=1
        print(file,counter)
        Combine= Combine.append(df)
    Combine['ITEM']=Combine['ITEM'].apply(int)
    Joined =pd.merge(Combine,Item_Category, on='ITEM', how='left', indicator=True)
    df= Joined[filted_columns_name]
    df['WEEKDAY'] = df.apply(lambda row: (row["DOB"].weekday())+1, axis=1)
    df["SALES"]   = df.apply(lambda row : row["PRICE"]*row["QUANTITY"],axis=1)
    df["OUNCES"]   = df.apply(lambda row : row["OUNCE"]*row["QUANTITY"],axis=1)
    Choc_Modifier=df[df["ITEM"]==10085]
    Custard_bar_count=df[df["ITEM"]==6110].ITEM.count()/6
    df= df[df["OUNCE"].notnull()]
    Modifed_Ratio = (Choc_Modifier.ITEM.count()-Custard_bar_count)/df.ITEM.count()
    print("The Modifed Ratio is:",Modifed_Ratio*100,"%" )
    return df,Modifed_Ratio

def MixAverage():
    df,Modifed_Ratio=preprocessing()
    ounces=df.groupby(["DOB","WEEKDAY","HOUR","CUSTARD_TYPE"])["OUNCES"].sum().reset_index()
    treats=df.groupby(["DOB","WEEKDAY","HOUR","CUSTARD_TYPE"])["QUANTITY"].sum().reset_index()
    MixSale_average= df.groupby(["DOB"])["SALES"].sum().reset_index().mean()
    a=treats.groupby(["HOUR","CUSTARD_TYPE"])["QUANTITY"].mean().reset_index()
    b=ounces.groupby(["HOUR","CUSTARD_TYPE"])["OUNCES"].mean().reset_index()
    Output =pd.merge(a,b, on=["HOUR", "CUSTARD_TYPE"], how='left', indicator=True)
    chocolate = Output.groupby(['CUSTARD_TYPE']).get_group('chocolate').rename(columns={'CUSTARD_TYPE':'Chocolate',"QUANTITY":"Treats_C","OUNCES":"OUNCES_C"})
    vanilla= Output.groupby(['CUSTARD_TYPE']).get_group('vanilla').rename(columns={'CUSTARD_TYPE':'Vanilla',"QUANTITY":"Treats_V","OUNCES":"OUNCES_V"})
    chocolate["Treats_C"] = chocolate.apply(lambda row : row["Treats_C"]*(1+Modifed_Ratio),axis=1)
    chocolate["OUNCES_C"] = chocolate.apply(lambda row : row["OUNCES_C"]*(1+Modifed_Ratio),axis=1)
    vanilla["OUNCES_V"] = vanilla.apply(lambda row : row["OUNCES_V"]*(1-Modifed_Ratio),axis=1)
    vanilla["Treats_V"] = vanilla.apply(lambda row : row["Treats_V"]*(1-Modifed_Ratio),axis=1)
    Mixresult= pd.merge(vanilla,chocolate, on='HOUR', how='left')
    Mixresult["Buckets_V"] = Mixresult.apply(lambda row : row["OUNCES_V"]/(128*3),axis=1)
    Mixresult["Buckets_C"] = Mixresult.apply(lambda row : row["OUNCES_C"]/(128*3),axis=1)
    Mix = Mixresult[['HOUR','Treats_V', 'OUNCES_V','Buckets_V','Treats_C', 'OUNCES_C','Buckets_C']]
    return Mix, MixSale_average

def Prediction(UserInput):
    Mix, MIXSALE_average = MixAverage()
    ratio = float(UserInput /MIXSALE_average)
    result= pd.concat([Mix.iloc[:,0:1],Mix.iloc[:,1:]*ratio],axis=1)
    result['Treats_V'] = result['Treats_V'].fillna(0.0).apply(math.ceil)
    result['OUNCES_V'] = result['OUNCES_V'].fillna(0.0).apply(math.ceil)
    result['Treats_C'] = result['Treats_C'].fillna(0.0).apply(math.ceil)
    result['OUNCES_C'] = result['OUNCES_C'].fillna(0.0).apply(math.ceil)
    result['Buckets_C'] = result['Buckets_C'].fillna(0.0).round(2)
    result['Buckets_V'] = result['Buckets_V'].fillna(0.0).round(2)
    total = result.apply(np.sum).round(2)
    total['HOUR'] = 'Total'
    result= result.append(pd.DataFrame(total.values, index=total.keys()).T, ignore_index=True)
    return result

def Prediction_half(UserInput):
    df,Modifed_Ratio =preprocessing()
    df.ix[df.MINUTE >= 30, 'MINUTE'] = 30
    df.ix[df.MINUTE < 30, 'MINUTE'] = 0
    ounces=df.groupby(["DOB","WEEKDAY","HOUR","MINUTE","CUSTARD_TYPE"])["OUNCES"].sum().reset_index()
    treats=df.groupby(["DOB","WEEKDAY","HOUR","MINUTE","CUSTARD_TYPE"])["QUANTITY"].sum().reset_index()
    MixSale_average= df.groupby(["DOB"])["SALES"].sum().reset_index().mean()
    a=treats.groupby(["HOUR","MINUTE","CUSTARD_TYPE"])["QUANTITY"].mean().reset_index()
    b=ounces.groupby(["HOUR","MINUTE","CUSTARD_TYPE"])["OUNCES"].mean().reset_index()
    Output =pd.merge(a,b, on=["HOUR","MINUTE","CUSTARD_TYPE"], how='left', indicator=True)
    chocolate = Output.groupby(['CUSTARD_TYPE']).get_group('chocolate').rename(columns={'CUSTARD_TYPE':'Chocolate',"QUANTITY":"Treats_C","OUNCES":"OUNCES_C"})
    vanilla= Output.groupby(['CUSTARD_TYPE']).get_group('vanilla').rename(columns={'CUSTARD_TYPE':'Vanilla',"QUANTITY":"Treats_V","OUNCES":"OUNCES_V"})
    chocolate["Treats_C"] = chocolate.apply(lambda row : row["Treats_C"]*(1+Modifed_Ratio),axis=1)
    chocolate["OUNCES_C"] = chocolate.apply(lambda row : row["OUNCES_C"]*(1+Modifed_Ratio),axis=1)
    vanilla["OUNCES_V"] = vanilla.apply(lambda row : row["OUNCES_V"]*(1-Modifed_Ratio),axis=1)
    vanilla["Treats_V"] = vanilla.apply(lambda row : row["Treats_V"]*(1-Modifed_Ratio),axis=1)   
    Mixresult= pd.merge(vanilla,chocolate, on=['HOUR','MINUTE'], how='left')
    Mixresult["Buckets_V"] = Mixresult.apply(lambda row : row["OUNCES_V"]/(128*3),axis=1)
    Mixresult["Buckets_C"] = Mixresult.apply(lambda row : row["OUNCES_C"]/(128*3),axis=1)
    Mixresult["HOUR"] = Mixresult["HOUR"].astype(str) + ":" +Mixresult["MINUTE"].astype(str)
    Mix = Mixresult[['HOUR','Treats_V', 'OUNCES_V','Buckets_V','Treats_C', 'OUNCES_C','Buckets_C']].fillna(0.0) 
    ratio = float(UserInput /MixSale_average)
    result= pd.concat([Mix.iloc[:,0:1],Mix.iloc[:,1:]*ratio],axis=1)
    result['Treats_V'] = result['Treats_V'].apply(math.ceil)
    result['OUNCES_V'] = result['OUNCES_V'].apply(math.ceil)
    result['Treats_C'] = result['Treats_C'].apply(math.ceil)
    result['OUNCES_C'] = result['OUNCES_C'].apply(math.ceil)
    result['Buckets_C'] = result['Buckets_C'].round(2)
    result['Buckets_V'] = result['Buckets_V'].round(2)
    total = result.apply(np.sum)
    total['HOUR'] = 'Total'
    result= result.append(pd.DataFrame(total.values, index=total.keys()).T, ignore_index=True)
    return result
