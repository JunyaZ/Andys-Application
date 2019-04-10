#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 11 12:16:44 2018

@author: Junya
"""
import pandas as pd
import glob
import os 
#from simpledbf import Dbf5
from dbfread import DBF
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
from pathlib import Path
from matplotlib.ticker import PercentFormatter

full_path =Path.cwd()
obspath, filename = os.path.split(full_path)
path=obspath + "\\Data\\"
dailypath = obspath + "\\Data\\Westport_result\\Daily\\"
categorypath = obspath  +"\\Data\\Westport_result\\Category\\"
graphpath= obspath + "\\Graphs\\"

WEEKDAY= {0: "Sunday",1: "Monday", 2:"Tuesday",3: "Wednesday",
      4: "Thursday",5: "Friday",6: "Saturday"}        

def Graph1(CATEGORY):   
    for j in list(CATEGORY["DOB"].unique()):
        plt.figure(figsize=(10,8))
        fig=sns.barplot(data=CATEGORY[CATEGORY["DOB"]==j],y="CATEGORY_NAME",x="Percentage",palette ="deep")
        CATEGORY[CATEGORY["DOB"]==j].to_csv(categorypath + j +".csv",index=False)
        plt.xlim(0,100)
        for p in fig.patches:
            x_value = p.get_width()
            y_value = p.get_y() + p.get_height() / 2
            # Number of points between bar and label. Change to your liking.
            space = 5
            # Vertical alignment for positive values
            ha = 'left'
            # If value of bar is negative: Place label left of bar
            if x_value < 0:
                # Invert space to place label to the left
                space *= -1
                # Horizontally align label at right
                ha = 'right'        
            # Use X value as label and format number with one decimal place
            label = '{0:.1%}'.format(x_value/100)      
            # Create annotation
            plt.annotate(
                label,                      # Use `label` as label
                (x_value, y_value),         # Place label at end of the bar
                xytext=(space, 0),          # Horizontally shift label by `space`
                textcoords="offset points", # Interpret `xytext` as offset in points
                va='center',fontsize=20,                # Vertically center label
                ha=ha)                      # Horizontally align label differently for
                                    # positive and negative values.
        fig.legend(loc='upper center',ncol=6,prop={'size': 35})
        fig.set_xlabel(' ')
        fig.set_ylabel(' ')
        plt.yticks(size=20)
        plt.xticks(size=26)
        whichday= WEEKDAY[datetime.datetime.strptime(j, '%Y-%m-%d').weekday()]                        
        plt.title("Percentage of Category on " + j + " " + whichday,fontsize=20)
        plt.savefig(graphpath +"CategoryPercentage"+ j +" " + whichday+".png",bbox_inches='tight')
        plt.show()
def Graph2(HOUR):    
    for i in list(HOUR["DOB"].unique()):
        plt.figure(figsize=(35,10))
        fig=sns.barplot(data=HOUR[HOUR["DOB"]==i],y="Percentage",x="HOUR",hue="CATEGORY_NAME",palette ="muted")
        fig.legend(loc='upper left', bbox_to_anchor=(0, 1.0),ncol=3, fancybox=True, shadow=True)
        HOUR[HOUR["DOB"]==i].to_csv(dailypath +i+".csv",index=False)
        whichday= WEEKDAY[datetime.datetime.strptime(i, '%Y-%m-%d').weekday()]
        fig.legend(loc='best', ncol=6,prop={'size': 23})
        plt.yticks(size=26)
        plt.xticks(size=26)
        fig.set_xlabel(' ')
        fig.set_ylabel(' ')
        plt.ylim(0,0.2)
        plt.vlines(0.5, ymin=0, ymax=100,linestyles='dotted')
        plt.vlines(1.5, ymin=0, ymax=100,linestyles='dotted')
        plt.vlines(2.5, ymin=0, ymax=100,linestyles='dotted')
        plt.vlines(3.5, ymin=0, ymax=100,linestyles='dotted')
        plt.vlines(4.5, ymin=0, ymax=100,linestyles='dotted')
        plt.vlines(5.5, ymin=0, ymax=100,linestyles='dotted')
        plt.vlines(6.5, ymin=0, ymax=100,linestyles='dotted')
        #plt.vlines(7.0, ymin=0, ymax=100,linestyles='dotted')
        plt.vlines(7.5, ymin=0, ymax=100,linestyles='dotted')
        #plt.vlines(8.0, ymin=0, ymax=100,linestyles='dotted')
        plt.vlines(8.5, ymin=0, ymax=100,linestyles='dotted')
        #plt.vlines(9.0, ymin=0, ymax=100,linestyles='dotted')
        plt.vlines(9.5, ymin=0, ymax=100,linestyles='dotted')
        #plt.vlines(10.0, ymin=0, ymax=100,linestyles='dotted')
        plt.vlines(10.5, ymin=0, ymax=100,linestyles='dotted')
        #plt.vlines(11, ymin=0, ymax=100,linestyles='dotted')
        plt.vlines(11.5, ymin=0, ymax=100,linestyles='dotted')
        #plt.vlines(12, ymin=0, ymax=100,linestyles='dotted')
        plt.vlines(12.5, ymin=0, ymax=100,linestyles='dotted')
        #plt.vlines(13, ymin=0, ymax=100,linestyles='dotted')
        plt.vlines(13.5, ymin=0, ymax=100,linestyles='dotted')
        plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
        plt.title("Hourly Sales for each Category on " + i + " " + whichday,fontsize =60)
        plt.savefig(graphpath +"HourlySales"+ i + " "+ whichday +".png",bbox_inches='tight') 
if __name__ == "__main__":
    df= pd.read_csv(path+ "ItemData.csv")
    data= df[df["ITEM_NAME"].notnull()]
    file = data[data["CATEGORY_NAME"]!="Catering"]
    file["DateTime"] = file.apply(lambda x: datetime.datetime.strptime(x["DOB"], '%Y-%m-%d'),axis=1)
    CATEGORY=file.groupby(["DOB","WEEKDAY","CATEGORY_NAME"])["SALES"].sum().reset_index()
    TOTAL_SALES =CATEGORY.groupby(["DOB","WEEKDAY"])["SALES"].sum().reset_index().rename(columns={'SALES':'SALES_TOTAL'})
    NEW_CATEGORY=pd.merge(CATEGORY,TOTAL_SALES, on='DOB', how='left', indicator=True)
    NEW_CATEGORY["Percentage"] = NEW_CATEGORY.apply(lambda row: (row["SALES"]/row["SALES_TOTAL"]*100),axis=1)
#-------------------------------------------------------------------------------------------------------------------#       
    TOTAL_HOURSALES=file.groupby(["DOB","WEEKDAY"])["SALES"].sum().reset_index().rename(columns={'SALES':'TOTAL_HOURSALES'})
    HOURSALES=file.groupby(["DOB","WEEKDAY","CATEGORY_NAME","HOUR"])["SALES"].sum().reset_index()
    NEW_HOUR =pd.merge(HOURSALES,TOTAL_HOURSALES, on=['DOB'], how='left', indicator=True)
    NEW_HOUR["Percentage"] = NEW_HOUR.apply(lambda row: (row["SALES"]/row["TOTAL_HOURSALES"]),axis=1)
    #Graph1(NEW_CATEGORY)
    Graph2(NEW_HOUR)

