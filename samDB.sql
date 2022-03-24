##Create the DB 

CREATE DATABASE samDB; 

GRANT ALL PRIVILEGES ON samDB.* to 'sc3sam'@'localhost' IDENTIFIED BY '****'; 
GRANT ALL PRIVILEGES ON samDB.* to 'sc3sam'@'%s' IDENTIFIED BY '****'; 

USE samDB; 


CREATE TABLE events ( eventID VARCHAR(80), latitude DOUBLE(8,4), longitude DOUBLE(8,4), description VARCHAR(200), magVal DOUBLE(6,3), magType VARCHAR(20),timestampSec DATETIME, timestampNow DATETIME, depth DOUBLE(12,4), status VARCHAR(20), revision INT(10), localizacion VARCHAR(200), horaLocal DATETIME, PRIMARY KEY (eventID) ); 



