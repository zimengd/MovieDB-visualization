#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 17:57:58 2019

@author: apple
"""
import sqlite3
import pandas as pd

DBNAME = "data/movie.db"
movie_csv = "data/movie_info.csv"
genre_csv = "data/genre_id.csv"
movie_id_csv = "data/movie_id.csv"

def init_db():
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    
    # Drop tables
    statement = '''
        DROP TABLE IF EXISTS 'MovieInfo';
    '''
    cur.execute(statement)
    statement = '''
        DROP TABLE IF EXISTS 'Genre';
    '''
    cur.execute(statement)

    conn.commit()
    statement = '''
        CREATE TABLE 'Genre' (
                'id'INTEGER PRIMARY KEY AUTOINCREMENT,
                'genre_id' INTEGER,
                'genre_name' TEXT NOT NULL
        );
    '''
    cur.execute(statement)
    conn.commit()
    
    statement = '''
        CREATE TABLE 'MovieInfo' (
            'id' INTEGER PRIMARY KEY AUTOINCREMENT,
            'movieDB_id' INTEGER NOT NULL,
            'title' TEXT NOT NULL,
            'status' TEXT,
            'production_country1_name' TEXT,
            'number_of_production_countries' INTEGER NOT NULL,
            "spoken_language1_name" TEXT,
            'number_of_spoken_languages' INTEGER NOT NULL,
            'vote_average' REAL,
            'vote_count' INTEGER,
            "genre1_id" INTEGER,
            "number_of_genres" INTEGER,
            'runtime' INTERGER,
            "budget" INTEGER,
            "popularity" REAL,
            "revenue" REAL,
            
            FOREIGN KEY ('genre1_id')
                REFERENCES 'Genre' ('id')
        );
    '''
    cur.execute(statement)
    conn.close()
    
def import_data(fname,tname):
    conn = sqlite3.connect(DBNAME)
    df = pd.read_csv(fname)
    df.to_sql(tname,conn,if_exists='append', index=False)
    conn.commit()
    conn.close()
    
def set_db():
    init_db()
    import_data(movie_csv,"MovieInfo")
    import_data(genre_csv,"Genre")
    print("Set up successfully")
    
if __name__=="__main__":
    set_db()
    