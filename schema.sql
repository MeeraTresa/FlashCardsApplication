-- Initialize the database
-- Drop any existing data and create empty tables
DROP TABLE IF EXISTS cards;
DROP TABLE IF EXISTS users;
CREATE TABLE cards(
                    id              INTEGER PRIMARY KEY AUTOINCREMENT,
                    question        TEXT NOT NULL,
                    answer          TEXT NOT NULL
)
CREATE TABLE users(
                    id              INTEGER PRIMARY KEY AUTOINCREMENT,
                    username        TEXT NOT NULL UNIQUE,
                    email           STRING NOT NULL UNIQUE,
                    description     TEXT,
                    location        STRING NOT NULL,
                    password        TEXT NOT NULL
)