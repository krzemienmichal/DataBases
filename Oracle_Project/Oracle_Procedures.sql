CREATE OR REPLACE TRIGGER check_email 
BEFORE INSERT OR UPDATE ON CLIENT
REFERENCING  NEW AS NEW OLD AS OLD
FOR EACH ROW
BEGIN
    IF(:new.email NOT LIKE '%_@__%.___%')
    THEN
        RAISE_APPLICATION_ERROR(-20000, 'Incorret email addres');
    END IF;
END;

create or replace PROCEDURE ADDCLIENT 
(
  FN IN VARCHAR2 
, LN IN VARCHAR2 
, BD IN VARCHAR2 
, EL IN VARCHAR2 
, USRNM IN VARCHAR2 
, PSWD IN VARCHAR2 
) AS 
BEGIN
INSERT INTO client
VALUES(NULL,FN, LN, to_date(BD,'YYYY-MM-DD'), EL, USRNM, PSWD);
END ADDCLIENT;

create or replace NONEDITIONABLE PROCEDURE UpdateClient
(
    C_ID IN INT,
    fn IN VARCHAR2,
    ln IN VARCHAR2,
    bd IN VARCHAR2,
    El IN VARCHAR2,
    Usrnm VARCHAR2
)
IS
BEGIN
UPDATE client SET
FirstName = fn,
LastName = ln,
BirthDate = to_date(bd, 'YYYY-MM-DD'),
Email = El,
Username = Usrnm
WHERE client.Client_ID = C_ID;
END;

CREATE OR REPLACE PROCEDURE delete_client (c_id IN INT)
AS
BEGIN
DELETE FROM client where client.client_id = c_id;
END;

CREATE OR REPLACE PROCEDURE change_password (c_id IN INT,pas IN VARCHAR)
AS
BEGIN
UPDATE client
SET password = pas
WHERE client.client_id = c_id;
END;

CREATE OR REPLACE PROCEDURE add_movie
    (tl IN VARCHAR2,
    rt IN VARCHAR2,
    dir IN VARCHAR2,
    pc IN VARCHAR2)
IS
BEGIN 
INSERT INTO movie
VALUES(NULL,tl, to_date(rt, 'HH24:MM:SS'), dir, pc);
END;

CREATE OR REPLACE PROCEDURE update_movie
    (tl IN VARCHAR2,
    rt IN VARCHAR2,
    dir IN VARCHAR2,
    pc IN VARCHAR2)
IS
BEGIN 
UPDATE movie
SET
title = tl,
runningtime = to_date(rt, 'HH24:MM:SS'),
director = dir,
productioncompany=pc;
END;

CREATE OR REPLACE PROCEDURE delete_movie
(m_id IN INT) IS
BEGIN
DELETE FROM movie
WHERE movie.movie_id = m_id;
END;

CREATE OR REPLACE PROCEDURE add_movie_genre(
m_title IN VARCHAR2,
gn IN VARCHAR2) AS
G_ID INT := 0;
M_ID INT := 0;
BEGIN
SELECT genre_id INTO G_ID from genre WHERE genre.genre = gn;
SELECT movie_id INTO M_ID FROM movie WHERE movie.title = m_title;
INSERT INTO movie_genre VALUES(M_ID, G_ID);
END;

CREATE OR REPLACE PROCEDURE rm_gen_movie(
m_title IN VARCHAR2,
gn IN VARCHAR2) AS
G_ID INT := 0;
M_ID INT := 0;
BEGIN
SELECT genre_id INTO G_ID from genre WHERE genre.genre = gn;
SELECT movie_id INTO M_ID FROM movie WHERE movie.title = m_title;
DELETE FROM movie_genre WHERE movie_id = M_ID AND genre_id = G_ID;
END;

CREATE OR REPLACE PROCEDURE add_genre(
    GN IN VARCHAR2)
AS 
BEGIN
INSERT INTO genre VALUES(NULL, GN);
END;

CREATE OR REPLACE PROCEDURE add_ptw(
usrnm IN VARCHAR2,
m_title IN VARCHAR2)
AS
M_ID INT :=0;
C_ID INT :=0;
BEGIN
SELECT client_id INTO C_ID FROM client WHERE username = usrnm;
SELECT movie_id INTO M_ID FROM movie WHERE title = m_title;
INSERT INTO plan_to_watch VALUES(C_ID, M_ID);
END;

CREATE OR REPLACE PROCEDURE rm_ptw(
usrnm IN VARCHAR2,
m_title IN VARCHAR2)
AS
M_ID INT :=0;
C_ID INT :=0;
BEGIN
SELECT client_id INTO C_ID FROM client WHERE username = usrnm;
SELECT movie_id INTO M_ID FROM movie WHERE title = m_title;
DELETE FROM plan_to_watch
WHERE client_id = C_ID AND movie_id = M_ID;
END;

CREATE OR REPLACE PROCEDURE add_watched(
usrnm IN VARCHAR2,
m_title IN VARCHAR2)
AS
M_ID INT :=0;
C_ID INT :=0;
BEGIN
SELECT client_id INTO C_ID FROM client WHERE username = usrnm;
SELECT movie_id INTO M_ID FROM movie WHERE title = m_title;
INSERT INTO watched VALUES(C_ID, M_ID);
END;

CREATE OR REPLACE PROCEDURE rm_watched(
usrnm IN VARCHAR2,
m_title IN VARCHAR2)
AS
M_ID INT :=0;
C_ID INT :=0;
BEGIN
SELECT client_id INTO C_ID FROM client WHERE username = usrnm;
SELECT movie_id INTO M_ID FROM movie WHERE title = m_title;
DELETE FROM watched
WHERE client_id = C_ID AND movie_id = M_ID;
END;