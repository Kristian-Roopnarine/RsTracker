#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import time
import pandas as pd
import numpy as np
from pandas import ExcelWriter
from pandas import ExcelFile
import re


# In[ ]:


class Data:
    def __init__(self,name,profit,day,hours,amount,method):
        self.name= name
        self.profit= profit
        self.day= pd.to_datetime(day)
        self.amount = amount
        self.method = method
        self.hours = hours
        
    def create_data_object():
        name,profit,day,hours,amount,method = input('Name of data? '), input('How much did you make? '),input('Date of profit? '),input('How many hours did this take? '),input('What was the amount that created this profit? '),input('What type of method was this? (Bossing,Slayer,Skiling, etc)')
        data = Data(name,profit,day,hours,amount,method)
        return data 
    
    def create_dict(self):
        return dict(Name = [self.name],
             Profit = [self.profit],
             Day= [self.day],
             Amount = [self.amount],
             Method= [self.method],
             Hours = [self.hours]
            )       


# In[ ]:


def add_item():
    data = Data.create_data_object()
    df = pd.DataFrame(data.create_dict())
    total_df.append(df)
    df = pd.concat(total_df,ignore_index=True)
    return df

def sort_item(dataframe):
    print('How would you like to search through your data?\n1.Name\n2.Profit\n3.Day\n4.Amount\n5.Method\n6.Hours')
    number = int(input('Number: '))
    sort = columns[number - 1]
    return dataframe.set_index(sort)

def edit_item(sorted_df):
    item = input('Which item do you want to edit: ')
    column = input('Which value do you want to edit: ')
    new_value = input('What is the new value: ')
    sorted_df.loc[item,column] = new_value
    return sorted_df.reset_index()
    
def delete_item(sorted_df):
    item = input('What item do you want to delete? (Input the value according to what you sorted by): ')
    sorted_df = sorted_df.drop(item,axis=0)
    return sorted_df.reset_index()


# In[ ]:


total_df = []
columns = ['Name','Profit','Day','Amount','Method','Hours']


# In[ ]:


while True:
    print("What would you like to do?\n1.Add Data\n2.Edit data\n3.Delete data\n4.End ")
    answer= input("")
    if answer == '1':
        df = add_item()
    elif answer == '2':
        df = sort_item(df)
        print(df)
        df = edit_item(df)
    elif answer == '3':
        df = sort_item(df)
        print(df)
        df = delete_item(df)
        print(df)
    elif answer == '4':
        break


# In[ ]:


df = df.reset_index()


# In[ ]:


df


# In[ ]:


final_df

