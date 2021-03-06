#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# In[2]:


class DataLoad:
    
    Skip_Rows_City_Time = 0
    Ski_Rows_State = 0
    BR_Cases_By_State = None
    BR_Cases_By_City = None
    BR_Cases_Total = None
    DemographicData = {}
    states = pd.read_csv("Instances/BR_States.csv",index_col=0)
    cities = pd.read_csv("Instances/BR_Cities_By_State.csv",encoding='utf-8',index_col=0).fillna(False)
    
    def __init__(self):
        #Imports the information from the .csv file
        df = pd.read_csv("https://raw.githubusercontent.com/wcota/covid19br/master/cases-brazil-cities-time.csv",
                         encoding="utf-8", parse_dates=['date'])
        df["city"] = df["city"].str.split("/").str.get(0)+"-"+df["city"].str.split("/").str.get(1)
       
        df2 = pd.read_csv("https://raw.githubusercontent.com/wcota/covid19br/master/cases-brazil-states.csv",
                         encoding="utf-8", parse_dates=['date'])
        df2["city"] = df2["city"].str.split("/").str.get(0)+"-"+df2["city"].str.split("/").str.get(1)
       
        #Saves the number of rows that are in memory
        self.Skip_Rows_City_Time = len(df.index)
        self.Ski_Rows_State = len(df2.index)
        
        #Makes hard copies from the temporary DataFrame
        self.BR_Cases_Total = df[df["state"] == "TOTAL"].copy()
        self.BR_Cases_By_City = df[df["state"] != "TOTAL"].copy()
        self.BR_Cases_By_State = df2[df2["state"] != "TOTAL"].copy()
        
        #Reindex the DataFrames
        self.BR_Cases_By_City.index = range(len(self.BR_Cases_By_City))
        self.BR_Cases_Total.index = range(len(self.BR_Cases_Total))
        self.BR_Cases_By_State.index = range(len(self.BR_Cases_By_State.index))
        
        for i in self.states["State"]:
            self.DemographicData[i]=pd.DataFrame(
                pd.read_csv("Instances/DemographicData/"+i+"DemographicData.csv",
                encoding="utf-8",index_col=0,dtype={"City":str,"Population":float,"Area":float,"Density":float}))
        
        self.DemographicData["BR"] = pd.read_csv("Instances/DemographicData/BRDemographicData.csv",
                                    encoding="utf-8",index_col=0,dtype={"State":str,"Population":float,
                                                                       "Area":float, "Density":float})
        
        del df
        del df2
        
    
    def __update__(self):
        #Import the informatiof from the .csv file, skiping
        #the rows that are already in memory
        df = pd.read_csv("https://raw.githubusercontent.com/wcota/covid19br/master/cases-brazil-cities-time.csv",
                         encoding="utf8",skiprows=range(1,self.Skip_Rows_City_Time), parse_dates=['date'])
        df["city"] = df["city"].str.split("/").str.get(0)+"-"+df["city"].str.split("/").str.get(1)
        df2 = pd.read_csv("https://raw.githubusercontent.com/wcota/covid19br/master/cases-brazil-states.csv",
                         encoding="utf-8", skiprows=range(1,self.Ski_Rows_State), parse_dates=['date'])
        df2["city"] = df2["city"].str.split("/").str.get(0)+"-"+df2["city"].str.split("/").str.get(1)
        #Updates the number of rows
        self.Skip_Rows_City_Time += len(df.index)
        self.Ski_Rows_State += len(df2.index)
        
        #Concatenates the new data to the dataframe
        self.BR_Cases_By_City = pd.concat([self.BR_Cases_Total,df[df["state"]!="TOTAL"]],ignore_index=True)
        self.BR_Cases_Total = pd.concat([self.BR_Cases_Total,df[df["state"]=="TOTAL"]],ignore_index=True)
        self.BR_Cases_By_State = pd.concat([self.BR_Cases_By_State,df2[df2["state"]!= "TOTAL"]],ignore_index=True)
        
        del df
        del df2
    
    def getDemographicDataValue(self,state,city,value):
        return self.DemographicData[state][self.DemographicData[state]["City"].values == city][value].values[0]
    
    def getStateDemographicDataValue(self,state,value):
        return self.DemographicData["BR"].loc[state][value]

