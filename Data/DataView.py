#!/usr/bin/env python
# coding: utf-8

# In[59]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

plt.style.use('seaborn')


# In[199]:


class DataVisualizing:
    
    Skip_Rows = 0
    BR_Cases_By_City = None
    BR_Cases_Total = None
    
    
    
    def __init__(self):
        #Imports the information from the .csv file
        df = pd.read_csv("https://raw.githubusercontent.com/wcota/covid19br/master/cases-brazil-cities-time.csv",
                         encoding="utf-8")
        df['date'] = pd.to_datetime(df['date'])
        
        #Saves the number of rows that are in memory
        self.Skip_Rows = len(df.index)
        
        #Makes hard copies from the temporary DataFrame
        self.BR_Cases_Total = df[df["state"] == "TOTAL"].copy()
        self.BR_Cases_By_City = df[df["state"] != "TOTAL"].copy()
        
        #Reindex the DataFrames
        self.BR_Cases_By_City.index = range(len(self.BR_Cases_By_City))
        self.BR_Cases_Total.index = range(len(self.BR_Cases_Total))
        
    
    def __update__(self):
        #Import the informatiof from the .csv file, skiping
        #the rows that are already in memory
        df = pd.read_csv("https://raw.githubusercontent.com/wcota/covid19br/master/cases-brazil-cities-time.csv",
                         enconding="utf8",skiprows=range(1,self.Skip_Rows))
        
	df['date'] = pd.to_datetime(df['date'])
        #Updates the number of rows
        self.Skip_Rows = self.Skip_Rows + len(df.index)
        
        #Concatenates the new data to the dataframe
        self.BR_Cases_By_City = pd.concat([self.BR_Cases_Total,df[df["state"]!="TOTAL"]],ignore_index=True)
        self.BR_Cases_Total = pd.concat([self.BR_Cases_Total,df[df["state"]=="TOTAL"]],ignore_index=True)
        
    
    def TemporalSeries(self,city = None):
        city = city.decode('utf-8')
        if (city == None) or (city not in self.BR_Cases_By_City["city"].values):
            raise ValueError("'City' does not correspond to any valid value")
        else:
            Figure, Axes = plt.subplots(figsize=(8,8))

            _temp = self.BR_Cases_By_City[self.BR_Cases_By_City["city"].values == city]
            Axes.plot_date("date","totalCases",data = _temp,linestyle="solid",label="Total Cases")
            Axes.plot_date("date","deaths",data=_temp,linestyle="solid", label="Total Deaths")

            Axes.set_title("Temporal Series")
            Axes.set_ylabel("Number",labelpad=10,fontsize=14)
            Axes.set_xlabel("Time (Days)",labelpad=10,fontsize=14)

            Figure.legend(loc="upper left",bbox_to_anchor=(0.1,0.97),fontsize=12)
            Figure.autofmt_xdate()
            Figure.tight_layout()

            return Figure
        


# In[201]:


data = DataVisualizing()
figure = data.TemporalSeries("São Paulo/SP")
figure.savefig("__temp/")


