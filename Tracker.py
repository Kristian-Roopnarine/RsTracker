import pandas as pd
import numpy as np
from pandas import ExcelWriter,ExcelFile
import re
import os
import time


class Data:

    def __init__(self,name,profit,day,hours,amount,method):
        self.name = name.title()
        self.profit = float(profit)
        self.day = pd.to_datetime(day)
        self.amount = amount
        self.method = method.title()
        self.hours = float(hours)

    def create_data_object():
        name,profit,day,hours,amount,method = input('Name of data? '), input('How much did you make? '),input('Date of profit? '),input('How many hours did this take? '),input('What was the amount that created this profit? '),input('What type of method was this? (Bossing,Slayer,Skiling, etc)')
        data = Data(name,profit,day,hours,amount,method)
        return data

    def create_dict(self):
        return dict(Name = [self.name],
            Profit= [self.profit],
            Day = [self.day],
            Amount = [self.amount],
            Method = [self.method],
            Hours= [self.hours])    

def add_item(total):
    data = Data.create_data_object()
    total.append(pd.DataFrame(data.create_dict()))
    return pd.concat(total,ignore_index=True,sort=False)

def sort_item(dataframe,col):
    print('How would you like to search through your data?\n1.Name\n2.Profit\n3.Day\n4.Amount\n5.Method\n6.Hours')
    number = int(input('Number: '))
    sort = col[number - 1]
    print(dataframe.sort_values(by = sort))
    return sort

def sort_by_date(dataframe):
    return dataframe.sort_values(by='Day',ascending=False)

def edit_item(dataframe,col):
    dataframe.set_index(sort_item(dataframe,col),inplace=True)
    print(dataframe)
    item = input('Which item do you want to edit: ')
    column = input('Which value do you want to edit: ')
    if column.title() in col:
        new_value = input('What is the updated value: ')
        try:
            new_value = float(new_value)
        except ValueError:
            new_value = new_value.title()
        dataframe.loc[item.title(),column.title()] = new_value
        return dataframe.reset_index()
    else:
        print('Sorry that value could not be found. Try again.')
        return dataframe.reset_index()

def delete_item(dataframe,col):
    sort_item(dataframe,col)
    item = input('What item do you want to delete: ')
    for i in range(len(col)):
        df_item = dataframe[dataframe[col[i]] == item.title()]
        item_index = df_item.index
        if len(item_index) > 1:
            print('Multiple %s logs found.' % item.title())
            print(df_item)
            delete = int(input('Which entry number would you like to delete?'))
            dataframe.drop(delete,inplace=True)
            dataframe.reset_index(drop=True,inplace=True)
            return dataframe
        elif len(item_index) == 1:
            dataframe.drop(item_index,inplace=True)
            dataframe.reset_index(drop=True,inplace=True)
            return dataframe
        else:
            print('________________')
            print('Item not found.')
            print('________________')
            return dataframe

def check_log(dataframe,col):
    print(dataframe)
    print('Do you want to sort the data? ')
    answer = input('')
    if answer.lower()[0] == 'y':
        sort_item(dataframe,col)

def save_to_excel(user_dataframe,log_dataframe,file):
    user_dataframe['Progress'] = log_dataframe['Profit'].sum()
    with pd.ExcelWriter(file) as writer:
        user_dataframe.to_excel(writer,sheet_name='User Goals')
        log_dataframe.to_excel(writer,sheet_name='Data Log')
        writer.save()

def read_goals(file,total):
    if os.path.isfile(file):
        user_dataframe = pd.read_excel(file,sheet_name='User Goals',index_col = 0)
        log_dataframe = pd.read_excel(file,sheet_name='Data Log',index_col=0)
        total.append(log_dataframe)
        name = user_dataframe.index[0]
        goal = user_dataframe['Goal'][0]
        started = user_dataframe['Starting'][0]
        progress = user_dataframe['Progress'][0]
        print('Welcome back %s.' % name)
        time.sleep(1)
        print('Let\'s see how your goal is going.')
        time.sleep(1)
        print('Your goal was %s gp.' % goal)
        time.sleep(1)
        print('You started with %s gp.' % started)
        time.sleep(1)
        print('You\'ve made %s gp.' % progress)
        print('Which leads you at a final cash stack of '+ str(started + progress) + ' gp.')
        return total,user_dataframe,log_dataframe
    else:
        print('No log data found. Let\'s make a new one.')
        name = input('What\'s your name?')
        goal = input('What\'s your gp goal?')
        started = input('How much are you starting with?')
        progress = 0
        total = []
        user_dataframe = pd.DataFrame({'Goal':[goal],'Starting':[started],'Progress':[progress]}, index = [name])
        log_dataframe = pd.DataFrame({})
        with pd.ExcelWriter(file) as writer:
            user_dataframe.to_excel(writer,sheet_name='User Goals')
            log_dataframe.to_excel(writer,sheet_name='Data Log')
            writer.save()
        return  total,user_dataframe,log_dataframe


def main():

    #set default params
    total_df = []
    columns = ['Name','Profit','Day','Amount','Method','Hours']
    filename = 'RSgoal.xlsx'
    user_df = None
    log_df = None

    total_df,user_df,log_df = read_goals(filename,total_df)

    #create loop to launch application
    while True:
        print('What would you like to do?\n1.Add Data\n2.Edit data\n3.Delete data\n4.Check/Sort\n5.End ')
        answer = input('Answer: ')
        if answer == '1':
            log_df = add_item(total_df)
            save_to_excel(user_df,sort_by_date(log_df),filename)
        elif answer == '2':
            print(log_df)
            log_df = edit_item(log_df,columns)
            save_to_excel(user_df,sort_by_date(log_df),filename)
        elif answer == '3':
            print(log_df)
            log_df = delete_item(log_df,columns)
            save_to_excel(user_df,sort_by_date(log_df),filename)
        elif answer == '4':
            check_log(log_df,columns)
        else:
            save_to_excel(user_df,sort_by_date(log_df),filename)
            break    


main()