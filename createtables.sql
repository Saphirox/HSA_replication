CREATE DATABASE manyusers;
USE manyusers;

CREATE TABLE users (
    id INT NOT NULL AUTO_INCREMENT,
    first_name varchar(255),
    last_name varchar(255),
    email varchar(255),
    birth_date varchar(255),
    gender varchar(255),
    PRIMARY KEY (id)
);