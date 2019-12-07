#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 20:50:27 2019

@author: apple
"""
from data_prep import data_prep
from database import set_db
import data_visual
from plotly.offline import plot

hist_lst = ["vote_count","number_of_genres",
                "number_of_production_countries",""]
scatter_lst = ["budget","revenue","popularity","vote_average",""]
pie_lst = ["genre","production_country","spoken_language",""]
bar_lst = ["genre","production_country","spoken_language",""]
c_lst= ["histogram","scatter","pie","bar"]

def print_help():
    with open('help.txt') as f:
        print(f.read())

def process_command(command):
    command_lst = command.split(" ")
    if command_lst[0] not in c_lst:
        return False
    #"histogram"
    if command_lst[0] == "histogram":
        if len(command_lst) > 2:
            return False
        elif len(command_lst) == 2:
            if command_lst[1] not in hist_lst:
                return False
            else:
                fig = data_visual.histogram(command_lst[1])
        else:
            fig = data_visual.histogram()
    #"scatter"
    if command_lst[0] == "scatter":
        if len(command_lst) == 3:
            if command_lst[1] not in scatter_lst:
                return False
            if command_lst[2] not in scatter_lst:
                return False                
            fig = data_visual.scatter(command_lst[1],command_lst[2])
        elif len(command_lst) == 1:
            fig = data_visual.scatter()
        else:
            return False
    
    #pie
    if command_lst[0] == "pie":
        if len(command_lst) > 2:
            return False
        elif len(command_lst) == 2:
            if command_lst[1] not in pie_lst:
                return False
            else:
                fig = data_visual.piechart(command_lst[1])
        else:
            fig = data_visual.piechart()
    
    #bar
    if command_lst[0] == "bar":
        if len(command_lst) > 2:
            return False
        elif len(command_lst) == 2:
            if command_lst[1] not in bar_lst:
                return False
            else:
                fig = data_visual.bar(command_lst[1])
        else:
            fig = data_visual.bar()
    
    try:
        plot(fig)
    except:
        return False

def menu():
    print_help()
    response = ''
    while response != 'exit':
        response = input('Enter a command: ')

        if response == 'help':
            print_help()
        
        if response == 'update':
            data_prep()
            
        elif response == "set":
            set_db()
            
        elif response == 'exit':
            print("bye")
        else:
            if process_command(response) == False:
                print("Command not recognized:",response)    
                
            
if __name__=="__main__":
#if need to set up database, please uncomment following code
#    data_prep()
#    set_db()
    menu()