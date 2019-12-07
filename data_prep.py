#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 16:08:06 2019

@author: zimeng ding
"""
import requests
import json
from bs4 import BeautifulSoup
import pandas as pd
import json
from secret_data import API_KEY

page_url = "https://www.themoviedb.org/movie?language=en-US"
header = {'User-Agent': 'SI_CLASS'}

class movie:
    def __init__(self,movie_id,title):
        self.title = title
        self.movie_id = movie_id

class genre:
    def __init__(self,genre_id,genre_name ):
        self.genre_id = genre_id
        self.genre_name = genre_name
    

def make_request_using_cache(url, header = None): 
    if header != None:
        CACHE_FNAME = 'cache.json'
    else:
        CACHE_FNAME = 'api.json'
    try:
        cache_file = open(CACHE_FNAME, 'r')
        cache_contents = cache_file.read()
        CACHE_DICTION = json.loads(cache_contents)
        cache_file.close()
    
    except:
        CACHE_DICTION = {}
    
    unique_ident = url

    if unique_ident in CACHE_DICTION:
        print("Getting cached data...")
        return CACHE_DICTION[unique_ident]


    else:
        print("Making a request for new data...")
        # Make the request and cache the new data
        if header != None:
            resp = requests.get(url, headers=header)
        else:
            resp = requests.request("GET", url)
        CACHE_DICTION[unique_ident] = resp.text
        dumped_json_cache = json.dumps(CACHE_DICTION)
        fw = open(CACHE_FNAME,"w")
        fw.write(dumped_json_cache)
        fw.close() # Close the open file
        return CACHE_DICTION[unique_ident]    

def get_titles(page_url):
    page_text = make_request_using_cache(page_url, header)
    page_soup = BeautifulSoup(page_text, 'html.parser')
    content_div = page_soup.find_all(class_='item poster card')
    movie_list = []
    
    #get movie title and its id from one page
    for p in content_div:
        title = p.find(class_="flex").find('a').text
        movie_id = p.find(class_="flex").find('a')['id'].strip('movie_')
        m = movie(movie_id,title)
        movie_list.append(m)
    return movie_list

def get_pages():
    #scrape serveral pages
    movies_list = []
    movies_list += get_titles(page_url)
    for i in range(8):
        url = page_url+"&page="+str(i)
        movies_list += get_titles(url)
    
    return movies_list
    
def get_api(id):
    url = "https://api.themoviedb.org/3/movie/"
    url = url + str(id) + "?api_key=" + API_KEY
    response = make_request_using_cache(url)
    movie_obj = json.loads(response)
    
    #delete production_companies
    try:
        del movie_obj["production_companies"]
    except KeyError:
        pass
    
    #these following attribute may have a list of values
    #genre
    n = len(movie_obj["genres"])
    k = "number_of_genres"
    movie_obj.update({k:n})
    for i in range(1):
        k = "genre"+str(i+1)+"_id"
        try:
            v = movie_obj["genres"][i]['id']
        except:
            v = movie_obj["genres"]
        movie_obj.update({k:v})
    try:
        del movie_obj["genres"]
    except KeyError:
        pass
    
    #production_countries
    n = len(movie_obj["production_countries"])
    k = "number_of_production_countries"
    movie_obj.update({k:n})
    for i in range(n):
        k = "production_country"+str(i+1)+"_name"
        try:
            v = movie_obj["production_countries"][i]['name']
        except:
            v = movie_obj["production_countries"]
        movie_obj.update({k:v})
    try:
        del movie_obj["production_countries"]
    except KeyError:
        pass
    
    #spoken_languages
    n = len(movie_obj["spoken_languages"])
    k = "number_of_spoken_languages"
    movie_obj.update({k:n})
    for i in range(1):
        k = "spoken_language"+str(i+1)+"_name"
        #print(movie_obj["spoken_languages"])
        try:
            v = movie_obj["spoken_languages"][i]['name']
        except:
            v = movie_obj["spoken_languages"]
        movie_obj.update({k:v})
    try:
        del movie_obj["spoken_languages"]
    except KeyError:
        pass
    
    #delete useless attributes
    try:
        del movie_obj["release_date"]
        del movie_obj["original_title"]
        del movie_obj["original_language"]
        del movie_obj["overview"]
        del movie_obj["video"]
        del movie_obj["imdb_id"]
        del movie_obj["homepage"]
        del movie_obj["tagline"]
        del movie_obj["adult"]
        del movie_obj["backdrop_path"]
        del movie_obj["belongs_to_collection"]
        del movie_obj["poster_path"]
        del movie_obj["production_country2_name"]
        del movie_obj["production_country3_name"]
        del movie_obj["production_country4_name"]
                        
    except KeyError:
        pass
    
    
    keys = movie_obj.keys()
    vals = []
    v = []
    for k in keys:
        v.append(movie_obj[k])
    vals.append(v)
    df = pd.DataFrame(data = vals,columns = keys)
    df.rename(columns={'id':'movieDB_id'}, inplace=True)
    

    return df

    
def get_genre():
    url = "https://api.themoviedb.org/3/genre/movie/list?"
    url += "api_key="
    url += API_KEY 
    url += "&language=en-US"
    obj = json.loads(make_request_using_cache(url))
    obj_lst = obj["genres"]
    genre_lst = []
    for i in obj_lst:
        g = genre(i['id'],i['name'])
        genre_lst.append(g) 
        
    genre_id = []
    genre_name = []
    for g in genre_lst:
        genre_id.append(g.genre_id)
        genre_name.append(g.genre_name)
        
    df = pd.DataFrame()
    df['genre_id'] = genre_id
    df['genre_name'] = genre_name
    df.to_csv('genre_id.csv', encoding='utf-8', index=False)
    return genre_id,genre_name

def data_prep():
    movies_lst = get_pages()
    titles_lst = []
    for m in movies_lst:
        l = [m.movie_id,m.title]
        titles_lst.append(l)
    
    df = pd.DataFrame(titles_lst, columns = ['id','title'])
    
    # write into csv file
    df.to_csv('movie_id.csv', encoding='utf-8', index=False)
    
     #genre info
    get_genre()
    
    #get detailed info
    movie_id = df['id']
    df_lst = []
    for i in movie_id:
        df = get_api(i)
        df_lst.append(df)
    result = pd.concat(df_lst, ignore_index=True, sort=False)
    result.to_csv('movie_info.csv', encoding='utf-8', index=False)
    #len = 8
    return df_lst
    
    
if __name__=="__main__":
    data_prep()
    

   





