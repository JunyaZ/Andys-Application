# -*- coding: utf-8 -*-
"""
Created on Mon Jan 28 13:53:56 2019

@author: Junya
"""

import pandas as pd
import datetime


df =pd.read_csv("myReport.csv")
item =pd.read_csv("Item.csv")
df["Week"] = df.Date.apply(lambda row: datetime.datetime.strptime(row, '%m-%d-%Y').weekday()+1)
df['Week']=df['Week'].apply(int)
df=df[df["Week"]==1]
Joined =pd.merge(df,item, on='Item_ID', how='left', indicator=True)
