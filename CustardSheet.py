# -*- coding: utf-8 -*-
"""
Created on Wed Nov 21 09:49:56 2018

@author: Junya
"""
import pandas as pd
import datetime
import numpy as np
import os
import sys
import glob
import shutil
from simpledbf import Dbf5
import math

filted_columns_name = ['ITEM','ITEM_NAME','ITEM_SIZE','CATEGORY_NAME','PRICE','HOUR',
   'MINUTE','DOB','QUANTITY','DISCPRIC','OUNCE','CUSTARD_TYPE']
exclued_item=[30000,30005,30010,30015,30030,40001,40002,40003,40004,40005]
currentpath = sys.path[0]
output =currentpath+"\\Output"
datapath, folder = os.path.split(currentpath)

def roundPartial (value, resolution):
    return math.ceil (value /float(resolution)) * resolution
def my_round(x):
    return math.ceil(x*8)/8

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
    Item_Category= pd.read_csv(currentpath+"\\item.csv")
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
    df= df[~df["ITEM"].isin(exclued_item)]
    return df

def MixAverage(GroupFeatures):
    df=preprocessing()
    df['MINUTE'].values[df['MINUTE'].values >=30 ] = 30
    df['MINUTE'].values[df['MINUTE'].values <30 ] = 0
    MixSale_average= df.groupby(["DOB"])["SALES"].sum().reset_index().mean()
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
#    print("The MixSale_Average is :", MixSale_average)
    return Mix, MixSale_average


def Modification(result):
    result['Treats_V'] = result['Treats_V'].fillna(0.0).apply(math.ceil)
    result['OUNCES_V'] = result['OUNCES_V'].fillna(0.0).round(1)
    result['Treats_C'] = result['Treats_C'].fillna(0.0).apply(math.ceil)
    result['OUNCES_C'] = result['OUNCES_C'].fillna(0.0).round(1)
    result['Buckets_C'] = result['Buckets_C'].fillna(0.0)
    result['Buckets_V'] = result['Buckets_V'].fillna(0.0)
    result["Buckets_C"] = result.apply(lambda row : my_round(row["Buckets_C"]),axis=1)
    result["Buckets_V"] = result.apply(lambda row : my_round(row["Buckets_V"] ),axis=1)
    return result

def Prediction(UserInput):
    HOURLY= ["HOUR"]
    Mix, MIXSALE_average = MixAverage(HOURLY)
    ratio = float(UserInput /MIXSALE_average)
    com= pd.concat([Mix.iloc[:,0:1],Mix.iloc[:,1:]*ratio],axis=1)
    result=Modification(com)
    total = result.apply(np.sum).round(1)
    total['HOUR'] = 'Total'
    print("The prejected Sales vs Average Sale Ratio  is :",ratio)
    result= result.append(pd.DataFrame(total.values, index=total.keys()).T, ignore_index=True)
    print("result",result)
    return result

def Prediction_half(UserInput):
    HOURLY= ["HOUR","MINUTE"]
    Mix, MIXSALE_average = MixAverage(HOURLY)
    Mix["HOUR"] = Mix["HOUR"].astype(str) + ":" +Mix["MINUTE"].astype(str)
    Mix=Mix.drop(columns=['MINUTE'])
    ratio = float(UserInput /MIXSALE_average)
    com= pd.concat([Mix.iloc[:,0:1],Mix.iloc[:,1:]*ratio],axis=1)
    result=Modification(com)
    total=pd.DataFrame(result.iloc[:,1:].apply(np.sum).round(1)).rename(columns={0:"Total"}).T
    total["HOUR"]=total.index
    cols= total.columns.tolist()
    cols = cols[-1:] + cols[:-1]
    total=total[cols]
    print(total)
    print("The prejected Sales vs Average Sale Ratio  is :",ratio)
    result= result.append(total, ignore_index=True)
    print("result",result)
    return result
    