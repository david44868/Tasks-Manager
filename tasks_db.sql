/********************************************************
* This script creates the database named tasks_db
*********************************************************/

DROP DATABASE IF EXISTS tasks_db;
CREATE DATABASE tasks_db;
USE tasks_db;

-- create the tables for the database
CREATE TABLE users (
	user_id 			INT 			PRIMARY KEY 	AUTO_INCREMENT,
	username 			VARCHAR(60) 	NOT NULL
);


CREATE TABLE tasks (
	task_id				INT 			PRIMARY KEY 	AUTO_INCREMENT,
    user_id 			INT				NOT NULL,
    title				VARCHAR(60)		NOT NULL,
	description 		TEXT 			NOT NULL,
    status 				VARCHAR(60) 	NOT NULL,
    due_date			date			NOT NULL,
    CONSTRAINT tasks_fk_users
		FOREIGN KEY (user_id)
		REFERENCES users (user_id)
);