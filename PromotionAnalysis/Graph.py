#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 11 12:16:44 2018

@author: Junya
"""
import os
import pandas as pd
import glob
from simpledbf import Dbf5
from dbfread import DBF
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
from pathlib import Path
full_path =Path.cwd()
obspath, filename = os.path.split(full_path)
path=obspath + "\\Data\\"
weektrendspath= obspath +"\\Data\\TotalSalesTrends\\"
TotalsalesGraph = obspath + "\\Graphs\\TotalSales\\"
WEEKDAY= {0: "Sunday",1: "Monday", 2:"Tuesday",3: "Wednesday",4: "Thursday",5: "Friday",6: "Saturday"}
def Graph1(file):
    for i in list(WEEKDAY.keys()):
        DAY =file[file["WEEKDAY"]==i].groupby(["DOB","WEEKDAY"])["SALES"].sum().reset_index()
        DAY.to_csv(weektrendspath + WEEKDAY[i]+ ".csv",index=False)
        fig= sns.catplot(data=DAY, x="DOB", y="SALES",kind= "point",height=6,aspect=4)
        fig.set_xticklabels(rotation=0)
        plt.yticks(size=20)
        plt.xticks(size=15)
        plt.title(WEEKDAY[i]+ "Trends of Total Sales",fontsize= 35)
        plt.ylim(2000,7500)
        plt.savefig(TotalsalesGraph+ "Trends_" + WEEKDAY[i]+".png",bbox_inches ="tight")      
        plt.show()
def Graph2(CATEGORY):    
    for j in list(CATEGORY["DOB"].unique()):
        plt.figure(figsize=(30,6))
        fig=sns.barplot(data=CATEGORY[CATEGORY["DOB"]==j],x="CATEGORY_NAME",y="SALES",palette ="deep")
        for item in fig.get_xticklabels():
            item.set_rotation(0)
        for p in fig.patches:
            height = p.get_height()
            fig.text(p.get_x()+p.get_width()/2.,
                height + 50,
                '{:1.1f}'.format(height),
                ha="center",fontsize= 13) 
        fig.set_xlabel(' ')
        fig.set_ylabel(' ')
        plt.yticks(size=20)
        plt.xticks(size=15)
        plt.ylim(0,4600)
        plt.title( "Total Sales of Category on " + j + " " + WEEKDAY[datetime.datetime.strptime(j, '%Y-%m-%d').weekday()],fontsize=35)
        plt.savefig(TotalsalesGraph + "CategoryTotalSales_"+ j + " " + WEEKDAY[datetime.datetime.strptime(j, '%Y-%m-%d').weekday()],bbox_inches='tight')
        plt.show()
def Graph3(HOUR):    
    for j in list(HOUR["DOB"].unique()):
        plt.figure(figsize=(10,8))
        fig=sns.barplot(data=HOUR[HOUR["DOB"]==j],x="HOUR",y="SALES",palette ="deep")
        #totalsale=HOUR[HOUR["DOB"]==j]["SALES"].sum()
        for p in fig.patches:
            height = p.get_height()
            fig.text(p.get_x()+p.get_width()/2.,
                height + 5,
                '{:1.1f}'.format(height),
                ha="center") 
        fig.set_xlabel(' ')
        fig.set_ylabel(' ')
        plt.ylim(0,1500)
        plt.title(j + " " + WEEKDAY[datetime.datetime.strptime(j, '%Y-%m-%d').weekday()])
        plt.show()
        #plt.savefig("HourlySales"+ j + ".png")
def Graph4(file):
    month= {1:"January", 2:"February", 3:"March",4:"April",5:"May", 6:"June", 
            7:"July", 8:"August", 9:"September", 10:"October", 11:"November", 12:"December"}
    for i in range(8,12):
        MonthData = file[file['DateTime'].map(lambda x: x.month) == i]
        MonthData["Date"] = MonthData.apply(lambda x: x["DateTime"].day,axis=1)
        plt.figure(figsize=(30,8))
        fig=sns.barplot(data=MonthData,x='Date',y="SALES",palette ="GnBu_d")
        for p in fig.patches:
            height = p.get_height()
            fig.text(p.get_x()+p.get_width()/2.,
                height + 50,
                '{:1.1f}'.format(height),
                ha="center",fontsize= 14) 
        fig.set_xlabel(' ')
        fig.set_ylabel(' ')
        plt.title("Total Sales of " + month[i],fontsize= 35)
        plt.ylim(0,7500)
        plt.yticks(size=20)
        plt.xticks(size=15)
        plt.savefig(TotalsalesGraph + "TotalSales of "+ month[i] + ".png")
if __name__ == "__main__":
    df= pd.read_csv(path+ "ItemData.csv")
    data = df[df["CATEGORY_NAME"]!="Catering"]
    file= data[data["ITEM_NAME"].notnull()]
    file["DateTime"] = file.apply(lambda x: datetime.datetime.strptime(x["DOB"], '%Y-%m-%d'),axis=1)
    CATEGORY=file.groupby(["DOB","WEEKDAY","CATEGORY_NAME"])["SALES"].sum().reset_index()
    HOUR=file.groupby(["DOB","WEEKDAY","HOUR"])["SALES"].sum().reset_index()
    MONTH=file.groupby(["DateTime","DOB"])["SALES"].sum().reset_index()
    Graph1(file)
    #Graph2(CATEGORY)
    #Graph3(HOUR)
    #Graph4(MONTH)
    
