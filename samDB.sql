##Create the DB 

CREATE DATABASE samDB; 

GRANT ALL PRIVILEGES ON samDB.* to 'sc3sam'@'localhost' IDENTIFIED BY '****'; 

USE samDB; 

CREATE TABLE events ( eventID VARCHAR(80), latitude DOUBLE(6,6), longitude DOUBLE(6,6), description VARCHAR(200), magVal DOUBLE(6,6), magType VARCHAR(20),timestampSec DATE, timestampNow DATE, depth DOUBLE(10,6), status VARCHAR(20), revision INT(10), localizacion VARCHAR(200), horaLocal DATE, PRIMARY KEY (eventID) ); 