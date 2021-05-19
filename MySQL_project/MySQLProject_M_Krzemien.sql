/*!40000 DROP DATABASE IF EXISTS `mkproject`*/;

CREATE DATABASE mkproject;

USE `mkproject`;
DROP TABLE IF EXISTS `client`;
CREATE TABLE `client` (
`Client_ID` INT NOT NULL AUTO_INCREMENT,
`FirstName` VARCHAR(30) NOT NULL, 
`LastName` VARCHAR(50) NOT NULL,
`BirthDate` DATE NOT NULL,
`Email` VARCHAR(255) UNIQUE NOT NULL,
`Username` VARCHAR(50) UNIQUE NOT NULL,
`Password` VARCHAR(22) NOT NULL,
PRIMARY KEY(`Client_ID`))engine=InnoDB;

SET autocommit=0;
INSERT INTO `client` VALUES(1,'Marian', 'Nowak', '2000-05-07', 'mawak@gmail.com', 'mawak', 'password123'); 
INSERT INTO `client` VALUES(2,'Jerzy', 'Kloda', '1980-03-12', 'joda@gmail.com', 'jkloda', '123pass');
INSERT INTO `client` VALUES(3,'Eddward', 'Elric', '1990-10-21', 'fullmetal@gmail.com', 'haganero', 'philosopher233');
COMMIT;

DROP TABLE IF EXISTS `movie`;
CREATE TABLE `movie`(
`Movie_ID` INT NOT NULL AUTO_INCREMENT,
`Title` VARCHAR(60) UNIQUE NOT NULL,
`RunningTime` TIME NOT NULL,
`Director` VARCHAR(80) NOT NULL,
`ProductionCompany` VARCHAR(100) NOT NULL,
PRIMARY KEY(`Movie_ID`))engine=InnoDB;

SET autocommit=0;
INSERT INTO `movie` VALUES(1,'Avengers', '02:22:00', 'Joss Whedon', 'Marvel');
INSERT INTO `movie` VALUES(2,'Pet Semetary', '01:41:00', 'Kelvin Kolsh', 'Di Bonaventura Pictures');
INSERT INTO `movie` VALUES(3,'Shrek', '01:30:00', 'Andrew Adamson', 'DreamWorks');
COMMIT;

DROP TABLE IF EXISTS `genre`;
CREATE TABLE `genre`(
`Genre_ID` INT NOT NULL AUTO_INCREMENT,
`MovieGenre` VARCHAR(50) UNIQUE NOT NULL,
PRIMARY KEY(`Genre_ID`))engine=InnoDB;

SET autocommit=0;
INSERT INTO `genre` VALUES(1,'Action');
INSERT INTO `genre` VALUES(2,'Horror');
INSERT INTO `genre` VALUES(3,'Drama');
INSERT INTO `genre` VALUES(4,'SciFi');
INSERT INTO `genre` VALUES(5,'Animation');
INSERT INTO `genre` VALUES(6,'Comedy');
INSERT INTO `genre` VALUES(7,'Thriller');
COMMIT;

DROP TABLE IF EXISTS `movie-genre`;
CREATE TABLE `movie-genre`(
`Movie_ID` INT NOT NULL,
`Genre_ID` INT NOT NULL,
PRIMARY KEY(`Movie_ID`,`Genre_ID`),
FOREIGN KEY(`Movie_ID`) REFERENCES `movie`(`Movie_ID`) ON DELETE CASCADE ON UPDATE CASCADE,
FOREIGN KEY(`Genre_ID`) REFERENCES `genre`(`Genre_ID`) ON DELETE CASCADE ON UPDATE CASCADE)engine=InnoDB;

SET autocommit=0;
INSERT INTO `movie-genre` VALUES(1,1);
INSERT INTO `movie-genre` VALUES(1,4);
INSERT INTO `movie-genre` VALUES(2,2);
INSERT INTO `movie-genre` VALUES(2,7);
INSERT INTO `movie-genre` VALUES(3,5);
INSERT INTO `movie-genre` VALUES(3,6);
COMMIT;

DROP TABLE IF EXISTS `watched`;
CREATE TABLE `watched`(
`Client_ID` INT NOT NULL,
`Movie_ID` INT NOT NULL,
PRIMARY KEY(`Client_ID`,`Movie_ID`),
FOREIGN KEY(`Client_ID`) REFERENCES `client`(`Client_ID`) ON DELETE CASCADE ON UPDATE CASCADE,
FOREIGN KEY(`Movie_ID`) REFERENCES `movie`(`Movie_ID`) ON DELETE CASCADE ON UPDATE CASCADE)engine=InnoDB;

SET autocommit=0;
INSERT INTO `watched` VALUES(1,2);
INSERT INTO `watched` VALUES(2,3);
INSERT INTO `watched` VALUES(1,1);
COMMIT;

DROP TABLE IF EXISTS `plantowatch`;
CREATE TABLE `plantowatch`(
`Client_ID` INT NOT NULL,
`Movie_ID` INT NOT NULL,
PRIMARY KEY(`Client_ID`,`Movie_ID`),
FOREIGN KEY(`Client_ID`) REFERENCES `client`(`Client_ID`) ON DELETE CASCADE ON UPDATE CASCADE,
FOREIGN KEY(`Movie_ID`) REFERENCES `movie`(`Movie_ID`) ON DELETE CASCADE ON UPDATE CASCADE)engine=InnoDB;

SET autocommit=0;
INSERT INTO `plantowatch` VALUES(1,3);
INSERT INTO `plantowatch` VALUES(2,1);
INSERT INTO `plantowatch` VALUES(3,1);
INSERT INTO `plantowatch` VALUES(3,2);
INSERT INTO `plantowatch` VALUES(3,3);
COMMIT;

CREATE VIEW list_ptw AS
SELECT `client`.Username, GROUP_CONCAT(`movie`.Title) as Plan_To_Watch
FROM `client`
JOIN `plantowatch` ON (`client`.Client_ID = `plantowatch`.Client_ID)
JOIN `movie` ON (`movie`.Movie_ID = `plantowatch`.Movie_ID)
GROUP BY `client`.Username;

CREATE VIEW list_watched AS
SELECT `client`.Username, GROUP_CONCAT(`movie`.Title) as Watched
FROM `client`
JOIN `watched` ON (`client`.Client_ID = `watched`.Client_ID)
JOIN `movie` ON (`movie`.Movie_ID = `watched`.Movie_ID)
GROUP BY `client`.Username;

CREATE VIEW list_movies AS
SELECT `movie`.*, GROUP_CONCAT(`genre`.MovieGenre) as Genre
FROM `movie`
LEFT JOIN `movie-genre` ON (`movie`.Movie_ID = `movie-genre`.Movie_ID)
LEFT JOIN genre ON (genre.Genre_ID = `movie-genre`.Genre_ID)
GROUP BY `movie`.Title;

CREATE VIEW list_genres AS
SELECT * FROM `genre`;

CREATE VIEW ListClients
AS SELECT * FROM `client`;

DELIMITER //
CREATE PROCEDURE SelectUserMovies (IN Username varchar(52))
BEGIN
SELECT `client`.Username,
(SELECT GROUP_CONCAT(`movie`.Title) FROM `movie` JOIN `plantowatch` ON (`movie`.Movie_ID = `plantowatch`.Movie_ID)
WHERE `plantowatch`.Client_ID = (SELECT `client`.Client_ID FROM `client` WHERE `client`.Username = Username) GROUP BY `plantowatch`.Client_ID ) AS `Plan To Watch`,
(SELECT GROUP_CONCAT(`movie`.Title) FROM `movie` JOIN `watched` ON (`movie`.Movie_ID = `watched`.Movie_ID)
WHERE `watched`.Client_ID = (SELECT `client`.Client_ID FROM `client` WHERE `client`.Username = Username) GROUP BY `watched`.Client_ID) AS `Watched`
FROM `client`
WHERE `client`.Username = Username ;
END//
DELIMITER ;

DELIMITER //
CREATE PROCEDURE AddClient (IN `fn` VARCHAR(30), IN `ln` VARCHAR(50),
IN `bd` DATE, IN `Email` VARCHAR(255), IN `Username` VARCHAR(50), IN `Password` VARCHAR(22))
BEGIN
INSERT INTO `client`(`FirstName`, `LastName`, `BirthDate`, `Email`, `Username`, `Password`)
VALUES(`fn`, `ln`, `bd`, `Email`, `Username`, `Password`);
END// 
DELIMITER ;

DELIMITER //
CREATE PROCEDURE UpdateClient (IN `Client_ID` INT, IN `fn` VARCHAR(30), IN `ln` VARCHAR(50),
IN `bd` DATE, IN `Email` VARCHAR(255), IN `Username` VARCHAR(50))
BEGIN
UPDATE `client` SET
FirstName = fn,
LastName = ln,
BirthDate = bd,
Email = Email,
Username = Username
WHERE `client`.Client_ID = `Client_ID`;
END//
DELIMITER ;

DELIMITER //
CREATE PROCEDURE ChagnePassword(IN ID INT, IN `Password` VARCHAR(30))
BEGIN
UPDATE `client` SET
`Password` = `Password`
WHERE `client`.Client_ID = ID;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE DeleteClient (IN ID INT)
BEGIN
DELETE FROM `client` WHERE `client`.Client_ID = ID;
END//
DELIMITER ;

DELIMITER //
CREATE PROCEDURE AddMovie(IN Title VARCHAR(50),
RunningTime TIME, Director VARCHAR(80),
ProductionCompany VARCHAR(100))
BEGIN
INSERT INTO `movie`(`Title`,`RunningTime`,`Director`,`ProductionCompany`)
VALUES(Title, RunningTime, Director, ProductionCompany);
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE AddGenreToMovie(IN Movie_Title VARCHAR(60), IN Genre VARCHAR(60))
BEGIN
DECLARE G_ID INT DEFAULT 0;
DECLARE M_ID INT DEFAULT 0;
SET G_ID = (SELECT `genre`.Genre_ID FROM `genre` WHERE `genre`.MovieGenre = Genre);
SET M_ID = (SELECT `movie`.Movie_ID FROM `movie` WHERE `movie`.Title = Movie_Title);
INSERT INTO `movie-genre` VALUES(`M_ID`, `G_ID`);
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE RemoveGenreFromMovie(IN Movie_Title VARCHAR(60), IN Genre VARCHAR(60))
BEGIN
DECLARE G_ID INT DEFAULT 0;
DECLARE M_ID INT DEFAULT 0;
SET G_ID = (SELECT `genre`.Genre_ID FROM `genre` WHERE `genre`.MovieGenre = Genre);
SET M_ID = (SELECT `movie`.Movie_ID FROM `movie` WHERE `movie`.Title = Movie_Title);
DELETE FROM `movie-genre` 
WHERE `movie-genre`.Movie_ID = M_ID AND `movie-genre`.Genre_ID = G_ID;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE UpdateMovie(IN ID INT, IN Title VARCHAR(50),
rt TIME, Dir VARCHAR(80), pc VARCHAR(100))
BEGIN
UPDATE `movie` SET
Title = Title,
RunningTime = rt,
Director = Dir,
ProductionCompany = pc
WHERE `movie`.Movie_ID = ID;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE DeleteMovie (IN ID INT)
BEGIN
DELETE FROM `movie` WHERE `movie`.Movie_ID = ID;
END//
DELIMITER ;

DELIMITER //
CREATE PROCEDURE AddGenre (IN Genre VARCHAR(60))
BEGIN
INSERT INTO `genre`(MovieGenre)
VALUES(Genre);
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE AddPtw (IN Username VARCHAR(60), IN M_Title VARCHAR(60))
BEGIN
DECLARE C_ID INT DEFAULT 0;
DECLARE M_ID INT DEFAULT 0;
SET C_ID = (SELECT `client`.Client_ID FROM `client` WHERE `client`.Username = Username);
SET M_ID = (SELECT `movie`.Movie_ID FROM `movie` WHERE `movie`.Title = M_Title);
INSERT INTO `plantowatch` VALUES(C_ID, M_ID);
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE RemovePtw (IN Username VARCHAR(60), IN M_Title VARCHAR(60))
BEGIN
DECLARE C_ID INT DEFAULT 0;
DECLARE M_ID INT DEFAULT 0;
SET C_ID = (SELECT `client`.Client_ID FROM `client` WHERE `client`.Username = Username);
SET M_ID = (SELECT `movie`.Movie_ID FROM `movie` WHERE `movie`.Title = M_Title);
DELETE FROM `plantowatch`
WHERE `plantowatch`.Client_ID = C_ID AND `plantowatch`.Movie_ID = M_ID;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE AddWatched (IN Username VARCHAR(60), IN Title VARCHAR(60))
BEGIN
DECLARE C_ID INT DEFAULT 0;
DECLARE M_ID INT DEFAULT 0;
SET C_ID = (SELECT `client`.Client_ID FROM `client` WHERE `client`.Username = Username);
SET M_ID = (SELECT `movie`.Movie_ID FROM `movie` WHERE `movie`.Title = M_Title);
INSERT INTO `watched` VALUES(C_ID, M_ID);
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE RemoveWatched (IN Username VARCHAR(60), IN Title VARCHAR(60))
BEGIN
DECLARE C_ID INT DEFAULT 0;
DECLARE M_ID INT DEFAULT 0;
SET C_ID = (SELECT `client`.Client_ID FROM `client` WHERE `client`.Username = Username);
SET M_ID = (SELECT `movie`.Movie_ID FROM `movie` WHERE `movie`.Title = Title);
DELETE FROM `plantowatch`
WHERE `watched`.Client_ID = C_ID AND `plantowatch`.Movie_ID = M_ID;
END //
DELIMITER ;



DELIMITER //
CREATE TRIGGER checkEmail
BEFORE INSERT ON `client` 
FOR EACH ROW BEGIN
DECLARE c_msg VARCHAR(256);
IF (NEW.Email NOT LIKE '%_@__%.__%')
THEN 
SET c_msg = "Cannot insert record because email addres is wrong";
SIGNAL SQLSTATE '13500'
SET MESSAGE_TEXT = c_msg;
END IF;
END //
DELIMITER ;

DELIMITER //
CREATE TRIGGER checkEmailBeforeUpdate
BEFORE UPDATE ON `client` 
FOR EACH ROW BEGIN
DECLARE c_msg VARCHAR(256);
IF (NEW.Email NOT LIKE '%_@__%.__%')
THEN 
SET c_msg = "Cannot update record because email addres is wrong";
SIGNAL SQLSTATE '13500'
SET MESSAGE_TEXT = c_msg;
END IF;
END //
DELIMITER ;

