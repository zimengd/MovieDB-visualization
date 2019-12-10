# SI507_final_project
Zimeng Ding
- To run the program, you only need to run user_interac.py, and follow the command menu or you could refer commands in help.txt.

- Scrape and crawl the first 8 pages under the “Movie” tab. And here is the link.
   - https://www.themoviedb.org/movie?language=en-US
   - Get the title and id of each movie and store them in a json file.
  
- Request the detailed information of each movie with cache by using the “the movie DB” API
  https://www.themoviedb.org/documentation/api?language=en-US
  
- data_prep.py : scrape pages, make API requests with cache and output data in csv files
  - two classes: movie(movie_id,title) and genre(genre_id,genre_name)
  - data process function: process_api(), data_prep()
  
- database.py : set up database using csv files
  - two tables: MovieInfo, Genre

- data_visual.py : show 4 kinds of charts
  - data process function: histogram(), scatter(), piechart(), bar()
  
- user_interac.py : print user interactive command line
  - data process function: process_command()
 
- final_proj_test.py : tests are only based on current cache files and database. if you update the data, tests might fail

- help.txt : command description


 
  
