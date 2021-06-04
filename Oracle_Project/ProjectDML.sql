alter session set nls_date_format = 'YY-MM-DD HH24:MI:SS';

INSERT INTO client VALUES(1,'Marian', 'Nowak', '2000-05-07', 'mawak@gmail.com', 'mawak', 'password123'); 
INSERT INTO client VALUES(2,'Jerzy', 'Kloda', '1980-03-12', 'joda@gmail.com', 'jkloda', '123pass');
INSERT INTO client VALUES(3,'Eddward', 'Elric', '1990-10-21', 'fullmetal@gmail.com', 'haganero', 'philosopher233');
INSERT INTO client VALUES(4,'Alphonse', 'Elric', '1993-11-21', 'armor@gmail.com', 'plateguy', 'philosopher133');
INSERT INTO client VALUES(5,'Andrzej', 'Zryw', '1992-01-21', 'zran@gmail.com', 'zrywan', 'haslo');
INSERT INTO client VALUES(6,'Edmund', 'Norwegia', '1987-05-11', 'norw@gmail.com', 'egi', 'pass');
INSERT INTO client VALUES(7,'Bjorn', 'Polaken', '1969-02-11', 'killer@gmail.com', 'headshot', 'oass3');
INSERT INTO client VALUES(8,'Oilander', 'Byk', '1999-11-06', 'oil@gmail.com', 'lander', 'phpher233');
INSERT INTO client VALUES(9,'War', 'Apocalipto', '1990-10-21', 'war@gmail.com','jerzy', 'psopher265');
INSERT INTO client VALUES(10,'Stefan', 'Tak', '1904-02-02', 'correct@gmail.com', 'approval', 'ppwa33');

INSERT INTO movie VALUES(1,'Avengers', to_date('02:22:00','HH24:MI:SS'), 'Joss Whedon', 'Marvel');
INSERT INTO movie VALUES(2,'Pet Semetary', to_date('01:41:00','HH24:MI:SS'), 'Kelvin Kolsh', 'Di Bonaventura Pictures');
INSERT INTO movie VALUES(3,'Shrek', to_date('01:30:00','HH24:MI:SS'), 'Andrew Adamson', 'DreamWorks');
INSERT INTO movie VALUES(4,'Shrek 2', to_date('01:32:00','HH24:MI:SS'), 'Andrew Adamson', 'DreamWorks');
INSERT INTO movie VALUES(5,'Shrek 3', to_date('01:33:00','HH24:MI:SS'), 'Chris Miller', 'DreamWorks');
INSERT INTO movie VALUES(6,'Thor:Rangarok', to_date('02:10:00','HH24:MI:SS'), 'Taiki Waititi', 'Marvel');
INSERT INTO movie VALUES(7,'Shining', to_date('02:26:00','HH24:MI:SS'), 'Stanley Kubrick', 'Warner Bros. Pictures');
INSERT INTO movie VALUES(8,'Treasure Planet', to_date('01:41:00','HH24:MI:SS'), 'Kelvin Kolsh', 'Di Bonaventura Pictures');
INSERT INTO movie VALUES(9,'Lalaland', to_date('02:06:00','HH24:MI:SS'), 'Damie Chazelle', 'Summit Entertainment');
INSERT INTO movie VALUES(10,'Dungeon and Dragons', to_date('02:22:00','HH24:MI:SS'), 'Courtney Solomon', 'Silver Pictures');
INSERT INTO movie VALUES(11,'Godzilla', to_date('01:20:00','HH24:MI:SS'), 'Tomoyuki Tanaka', 'Toho Studios');
INSERT INTO movie VALUES(12,'Shrek Forever', to_date('01:33:00','HH24:MI:SS'), 'Mike Mitchell', 'DreamWorks');

INSERT INTO genre VALUES(1,'Action');
INSERT INTO genre VALUES(2,'Horror');
INSERT INTO genre VALUES(3,'Drama');
INSERT INTO genre VALUES(4,'SciFi');
INSERT INTO genre VALUES(5,'Animation');
INSERT INTO genre VALUES(6,'Comedy');
INSERT INTO genre VALUES(7,'Thriller');

INSERT INTO movie_genre VALUES(1,1);
INSERT INTO movie_genre VALUES(1,4);
INSERT INTO movie_genre VALUES(2,2);
INSERT INTO movie_genre VALUES(2,7);
INSERT INTO movie_genre VALUES(3,5);
INSERT INTO movie_genre VALUES(3,6);
INSERT INTO movie_genre VALUES(4,2);
INSERT INTO movie_genre VALUES(4,5);
INSERT INTO movie_genre VALUES(5,1);
INSERT INTO movie_genre VALUES(5,7);
INSERT INTO movie_genre VALUES(6,2);
INSERT INTO movie_genre VALUES(6,4);
INSERT INTO movie_genre VALUES(7,3);
INSERT INTO movie_genre VALUES(7,2);

INSERT INTO watched VALUES(1,2);
INSERT INTO watched VALUES(2,3);
INSERT INTO watched VALUES(1,1);

INSERT INTO plan_to_watch VALUES(1,3);
INSERT INTO plan_to_watch VALUES(2,1);
INSERT INTO plan_to_watch VALUES(3,1);
INSERT INTO plan_to_watch VALUES(3,2);
INSERT INTO plan_to_watch VALUES(3,3);
