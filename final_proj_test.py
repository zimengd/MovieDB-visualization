#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 23:22:54 2019

@author: apple
"""

import data_prep
import database
import data_visual
import unittest

class TestDataPrep(unittest.TestCase):
    def test_get_genre(self):
        #4
        genre_id,genre_name = data_prep.get_genre()
        self.assertEqual(len(genre_id),19)
        self.assertEqual(len(genre_name),19)
        self.assertEqual(genre_name[0],"Action")
        self.assertEqual(genre_id[0],28)
    def test_get_title(self):
        #4
        movie_lst = data_prep.get_pages()
        self.assertEqual(len(movie_lst),160)
        self.assertEqual(movie_lst[0].movie_id,"330457")
        self.assertEqual(movie_lst[159].movie_id,"424783")
        self.assertEqual(movie_lst[159].title,"Bumblebee")
        
        
class TestDatabase(unittest.TestCase):
    def test_genre(self):
        #3
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()
        s = '''
        select "genre_id","genre_name" FROM Genre
        '''
        results = cur.execute(s)
        result_list = results.fetchall()
        self.assertIn((28,"Action"), result_list)
        self.assertIn((10402,"Music"), result_list)
        self.assertEqual(len(result_list), 19)
    def test_movie(self):
        #3
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()
        s = '''
        select "MovieDB_id","title" FROM MovieInfo
        '''
        results = cur.execute(s)
        result_list = results.fetchall()
        self.assertIn((475557,"Joker"), result_list)
        self.assertIn((487616,"Curiosa"), result_list)
        self.assertEqual(len(result_list), 160)
    
class TestDataVisual(unittest.TestCase):
    def test_visual(self):
        #if not return false, the function runs sucessfully
        try:
            histogram()
            scatter()
            piechart()
            bar()
        except:
            self.fail()
            
        
        


if __name__ == '__main__':
    unittest.main()