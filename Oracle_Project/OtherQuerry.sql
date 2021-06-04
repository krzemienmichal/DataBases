SELECT * FROM movie
OFFSET 4 ROWS
FETCH NEXT 2 ROWS ONLY;

SELECT * FROM movie
FETCH FIRST 4 ROWS ONLY; 

SELECT title, COUNT(watched.client_id) "Watchers"
FROM movie 
LEFT JOIN watched ON movie.Movie_ID = watched.Movie_ID
GROUP BY
ROLLUP(title); 



SELECT GENRE, COUNT(movie_genre.movie_id) as "Movies"
FROM GENRE
LEFT JOIN movie_genre ON genre.genre_id = movie_genre.genre_id
GROUP BY 
    CUBE(Genre)
ORDER BY
    genre NULLS LAST;
    
SELECT title, COUNT(watched.client_id) "Watchers",
RANK() OVER(ORDER BY COUNT(watched.client_id) DESC) AS "rank",
DENSE_RANK() OVER (ORDER BY COUNT(watched.client_id) DESC) AS "dense rank"
FROM movie 
LEFT JOIN watched ON movie.Movie_ID = watched.Movie_ID
GROUP BY title;
    
-- brak mo¿liwoœci wykonania zapytañ hierarchincznych ze wzglêdu na
-- brak wystêpowania hierarchii w bazie danych

SELECT username from client
MINUS
SELECT username from watched
LEFT JOIN client ON watched.client_id = client.client_id;


SELECT username from plan_to_watch
LEFT JOIN client ON plan_to_watch.client_id = client.client_id
INTERSECT
SELECT username from watched
LEFT JOIN client ON watched.client_id = client.client_id;