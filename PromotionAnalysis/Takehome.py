# -*- coding: utf-8 -*-
"""
Created on Wed Nov 28 16:50:37 2018

@author: Junya
"""

import pandas as pd
import glob
import os
from dbfread import DBF
from simpledbf import Dbf5
from pathlib import Path
import xlrd



full_path =Path.cwd()
obspath, filename = os.path.split(full_path)
datapath = obspath + "\\TakeHomePromotion\\"
salesDatapath = obspath + "\\TakeHomePromotion\\Sales\\"
CountsDatapath=obspath + "\\TakeHomePromotion\\Counts\\"
Costpath = obspath + "\\TakeHomePromotion\\Cost\\"
output = obspath + "\\TakeHomePromotion\\Output\\"
TotalPath = obspath +"\\TakeHomePromotion\\BOGO Take Home Weekly Data\\TotalSales\\"

#--------------------list----------------------------------#
ItemIDlist =[6010,6015,6020,6030,6035,6040,6045,6050,6055,6060,6065,6070,6075,6085,6120]

TestStoresDictionary={
1:"105 - Rogers",
2:"111 - Bolingbrook",
3:"112 - Joplin",
4:"115 - Fayetteville",
5:"116 - Countryside",
6:"117 - Burbank",
7:"120 - Westport",
8:"122 - Oak Lawn",
9:"124 - Lees Summit",
10:"126 - Evanston",
11:"129 - Blue Springs",
12:"135 - Oswego",
13:"138 - Grapevine",
14:"140 - N.  Richland  Hills",
15:"143 - Naper Crossing",
16:"148 - North Fort  Worth",
17:"149 - Mount  Prospect",
18:"153 - Naperville  North",
19:"730 - Sheridan",
20:"741 - Spring Hill",
21:"746 - Wichita",
22:"750 - Ahwatukee",
23:"751 -  Littleton"
}
ControlStoresDictionary= {
1:"101 - Sunshine",
2:"102 - Campbell",
3:"103 - Glenstone",
4:"104 - James River",
5:"108 - Branson",
6:"113 - Battlefield",
7:"139 - S. Glenstone"
}

DatesRame ={
"2017_1016_1022": "10/16-10/22/2017",
"2017_1023_1029" : "10/23-10/29/2017",
"2017_1030_1101" : "10/30-11/01/2017",
"2017_1102_1105" :"11/02-11/05/2017",
"2017_1106_1112" :"11/06-11/12/2017",
"2017_1113_1119" :"11/13-11/19/2017",
"2017_1120_1122" :"11/20-11/22/2017",
"2017_1123_1126" :"11/23-11/26/2017",
"2017_1127_1203" :"11/27-12/03/2017",
"2017_1204_1210" :"12/04-12/10/2017",

"2018_1015_1021" :"10/15-10/21",
"2018_1022_1028" :"10/22-10/28",
"2018_1029_1031" :"10/29-10/31",
"2018_1101_1104" :"11/01-11/04",
"2018_1105_1111" :"11/05-11/11",
"2018_1112_1118" :"11/12-11/18",
"2018_1119_1121" :"11/19-11/21",
"2018_1122_1125" :"11/22-12/25",
"2018_1126_1202" :"11/26-12/02",
"2018_1203_1209" :"12/03-12/09"
}        
def Calculation(globbed_file,ItemID):
    Result = pd.DataFrame()
    for file in globbed_file:
        wb = xlrd.open_workbook(file, logfile=open(os.devnull, 'w'))
        df= pd.read_excel(wb,index=False,skiprows=6,engine='xlrd')
        df= df[df["Unnamed: 0"]==ItemID]
        filtered = df[df.columns[~df.columns.str.contains('Unnamed:')]]
        Sum=pd.DataFrame(filtered.sum(0))
        Sum = Sum.rename(columns={0: file.split(sep="\\")[-1].split(sep=".")[0]})
        Result= pd.concat([Result,Sum],axis=1)
    return Result

def profit(file,data):
    wb = xlrd.open_workbook(file, logfile=open(os.devnull, 'w'))
    df= pd.read_excel(wb,index=False,skiprows=6,engine='xlrd')
    df=df.rename(columns={"Unnamed: 0": "ITEM"})
    df['ITEM']=df['ITEM'].apply(int)
    Joined =pd.merge(df,data, on='ITEM', how='right', indicator=True)
    filtered = Joined[Joined.columns[~Joined.columns.str.contains('Unnamed:|_merge')]]
    filtered = filtered.set_index(["ITEM"])
    Column= list(filtered.columns.values)
    filtered.to_excel(Costpath + file.split(sep="\\")[-1],index=False)
    for name in Column:
        filtered[name] = filtered.apply(lambda row: (row[name]*row["COST"]),axis=1)
    result =filtered[filtered.columns[~filtered.columns.str.contains("COST")]]  
    return result

def TotalCost(globbed_file,data,ItemID):
    Result = pd.DataFrame()
    for file in globbed_file:
        Total=profit(file,data)
        Total= Total[Total.index ==ItemID]
        Sum=pd.DataFrame(Total.sum(0))
        Sum = Sum.rename(columns={0: file.split(sep="\\")[-1].split(sep=".")[0]})
        Result= pd.concat([Result,Sum],axis=1)
    return Result

def StoreAverage(globbedfile,ItemIDlist,Dictionary):
    Itemaverage =pd.DataFrame()
    for ItemID in ItemIDlist:  
        Sales= Calculation(globbedfile,ItemID)
        ControlGroup =pd.DataFrame()
        for x in list(Dictionary.values()):
            Control = Sales[Sales.index ==x]
            ControlGroup = pd.concat([ControlGroup, Control])
        AverageControl = pd.DataFrame(ControlGroup.mean()).transpose()
        AverageControl.index.name =ItemID
        Itemaverage =pd.concat([Itemaverage, AverageControl])
    return Itemaverage

def CostStoreAverage(globbedfile,ItemIDlist,ItemCost,Dictionary):
    Itemaverage =pd.DataFrame()
    for ItemID in ItemIDlist:  
        Cost= TotalCost(globbedfile,ItemCost[['ITEM','COST']],ItemID)
        Cost.to_csv(output + str(ItemID) +".csv")
        ControlGroup =pd.DataFrame()
        for x in list(Dictionary.values()):
            Control = Cost[Cost.index ==x]
            ControlGroup = pd.concat([ControlGroup, Control])
        AverageControl = pd.DataFrame(ControlGroup.mean()).transpose()
        print(AverageControl)
        AverageControl.index.name =ItemID
        Itemaverage =pd.concat([Itemaverage, AverageControl])
    return Itemaverage
if __name__ == "__main__":  
    ItemCost =pd.read_excel(datapath +"Cost.xlsx")
    globbedSales = glob.glob(salesDatapath+"*.xls")
    globbedCounts =glob.glob(CountsDatapath+"*.xls")
    globbedTotal =glob.glob(TotalPath+"*.xls")
    #__________________________________________________________________#
    Control1 =StoreAverage(globbedSales,ItemIDlist,ControlStoresDictionary)
    Test1 = StoreAverage(globbedSales,ItemIDlist,TestStoresDictionary)
    Sales_Combined= Test1.append(Control1)
    Sales_Combined=Sales_Combined.rename(index=str, columns=DatesRame)
    
    CostControl=CostStoreAverage(globbedCounts,ItemIDlist,ItemCost[['ITEM','COST']],ControlStoresDictionary)
    CostTest=CostStoreAverage(globbedCounts,ItemIDlist,ItemCost[['ITEM','COST']],TestStoresDictionary)
    Cost_Combined= CostControl.append(CostTest)
    Cost_Combined=Cost_Combined.rename(index=str, columns=DatesRame)
    profit_Combined =Sales_Combined-Cost_Combined
    #__________________________________________________________________#    
#    writer = pd.ExcelWriter(output + "Promotation.xls")
#    Sales_Combined.to_excel(writer,"TakeHome"+ salesDatapath.split(sep="\\")[-2])
#    profit_Combined.to_excel(writer,"TakeHomeProfit")
#    totalSales_Combined.to_excel(writer,"TotalSales")
#    writer.save()
#     
