#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 15:49:42 2019

@author: apple
"""
import plotly.express as px
import plotly.graph_objs as go

import sqlite3
import pandas as pd

DBNAME = "movie.db"
    
def histogram(x= "vote_count"):
    statement = '''
SELECT "<>" FROM MovieInfo
'''
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
        
    s = statement.replace("<>",x)
    
    result = cur.execute(s).fetchall()
    col_name_list = [tuple[0] for tuple in cur.description]
    
    #to dataframe
    df = pd.DataFrame(columns = col_name_list,data = result)
    
    conn.commit()
    conn.close()
    
    fig = go.Figure()
    fig = px.histogram(df, x=x)
    
    return fig
    #plot(fig)
    
def scatter(x="budget",y = "revenue"):
    statement = '''
SELECT "<>", "[]","title" FROM MovieInfo
    '''
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    s = statement.replace("<>",x)
    s = s.replace("[]",y)
    
    result = cur.execute(s).fetchall()
    col_name_list = [tuple[0] for tuple in cur.description]
    
    #to dataframe
    df = pd.DataFrame(columns = col_name_list,data = result)
    
    conn.commit()
    conn.close()
    
    fig = go.Figure()
    fig = go.Figure(data=go.Scatter(
                                x=df[x],
                                y=df[y],
                                mode='markers',
                                marker = dict(
                                        size=12),
                                text=df['title'])) # hover text goes here
    
    fig.update_layout(title = x+'-'+y,
                      xaxis_title = x,
                      yaxis_title = y)
    return fig
    #plot(fig)

def piechart(x="genre"):
    statement = '''
SELECT "<>",count(MovieInfo.id) AS "count" FROM MovieInfo
GROUP BY "<>"
    '''
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    
    # genre needs to join table
    if x == "genre":
        s = '''
SELECT Genre.genre_name, count(MovieInfo.id) AS "count"
FROM Genre
LEFT JOIN MovieInfo where MovieInfo.genre1_id = Genre.genre_id
GROUP BY Genre.genre_name
'''
    else: 
        s = statement.replace("<>",x+"1_name")
    
    
    result = cur.execute(s).fetchall()
    
    col_name_list = [tuple[0] for tuple in cur.description]
    df = pd.DataFrame(columns = col_name_list,data = result)
    
    conn.commit()
    conn.close()
    try:
        labels = df[x+"1_name"]
    except:
        labels = df[x+"_name"]
    values = df["count"]

    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
    return fig
    #plot(fig)
    
def bar(x="genre"):
    statement = '''
SELECT "<>",count(MovieInfo.id) AS "count" FROM MovieInfo
GROUP BY "<>"
    '''
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    
    # genre needs to join table
    if x == "genre":
        s = '''
SELECT Genre.genre_name, count(MovieInfo.id) AS "count"
FROM Genre
LEFT JOIN MovieInfo where MovieInfo.genre1_id = Genre.genre_id
GROUP BY Genre.genre_name
'''
    else: 
        s = statement.replace("<>",x+"1_name")
    
    
    result = cur.execute(s).fetchall()
   
    col_name_list = [tuple[0] for tuple in cur.description]
    df = pd.DataFrame(columns = col_name_list,data = result)

    conn.commit()
    conn.close()
    try:
        dx = df[x+"1_name"]
    except:
        dx = df[x+"_name"]
    y = df["count"]

    fig = go.Figure([go.Bar(x=dx, y=y)])
    fig.update_layout(
                      xaxis_title = x,
                      yaxis_title = "count")
    return fig
    #plot(fig)


    
    
if __name__=="__main__":
    #histogram("number_of_production_countries")
    #histogram("number_of_genres")
    #histogram("vote_count") #nbin = 5
    #histogram("vote_count")
    #scatter("revenue","vote_average")
    #piechart("spoken_language")
    #piechart("production_country")
    #bar()
    #bar("spoken_language")
    #bar("production_country")
    pass    