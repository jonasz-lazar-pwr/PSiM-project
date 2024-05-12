-- Autorzy: Jonasz Lazar, Kacper Malinowski

DROP TABLE IF EXISTS UserAchievements;
DROP TABLE IF EXISTS Achievements;
DROP TABLE IF EXISTS Comments;
DROP TABLE IF EXISTS UserDwarfs;
DROP TABLE IF EXISTS Dwarfs;
DROP TABLE IF EXISTS Users;

DROP DATABASE IF EXISTS dwarfsDB;

CREATE DATABASE dwarfsDB;

CREATE TABLE Users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(64) NOT NULL,
    joined_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Dwarfs (
    dwarf_id INT PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    author VARCHAR(255) NOT NULL,
    address VARCHAR(255) NOT NULL,
    location VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    image_url TEXT NOT NULL
);

CREATE TABLE UserDwarfs (
    id SERIAL PRIMARY KEY,
    user_id INT,
    dwarf_id INT,
    visited_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (dwarf_id) REFERENCES Dwarfs(dwarf_id)
);

CREATE TABLE Comments (
    comment_id SERIAL PRIMARY KEY,
    user_id INT,
    dwarf_id INT,
    comment_text TEXT NOT NULL,
    comment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (dwarf_id) REFERENCES Dwarfs(dwarf_id)
);

CREATE TABLE Achievements (
    achievement_id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT NOT NULL
);

CREATE TABLE UserAchievements (
    id SERIAL PRIMARY KEY,
    user_id INT,
    achievement_id INT,
    achievement_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (achievement_id) REFERENCES Achievements(achievement_id)
);
