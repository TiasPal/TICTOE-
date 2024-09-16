CREATE DATABASE IF NOT EXISTS tic_tac_toe;
USE tic_tac_toe;

CREATE TABLE IF NOT EXISTS scores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    player CHAR(1) NOT NULL UNIQUE,
    wins INT DEFAULT 0,
    draws INT DEFAULT 0,
    losses INT DEFAULT 0
);

INSERT INTO scores (player) VALUES ('X') ON DUPLICATE KEY UPDATE player='X';
INSERT INTO scores (player) VALUES ('O') ON DUPLICATE KEY UPDATE player='O';
Select * from scores;