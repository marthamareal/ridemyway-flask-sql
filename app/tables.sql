 CREATE TABLE IF NOT EXISTS USERS  (
  ID SERIAL PRIMARY KEY NOT NULL,
  F_NAME VARCHAR(45) NOT NULL ,
  L_NAME VARCHAR(45) NOT NULL ,
  EMAIL  VARCHAR(50) NOT NULL UNIQUE ,
  CITY VARCHAR(50) NOT NULL ,
  PHONE_NO VARCHAR(25) NOT NULL ,
  PASSWORD VARCHAR(45) NOT NULL,
  LOGGED_IN BOOLEAN DEFAULT FALSE
 );
