-- Database schema

DROP TABLE IF EXISTS beer;
DROP TABLE IF EXISTS beer_category;
DROP TABLE IF EXISTS food;
DROP TABLE IF EXISTS snack;
DROP TABLE IF EXISTS worker;
DROP TABLE IF EXISTS worker_status;
DROP TABLE IF EXISTS shift;
DROP TABLE IF EXISTS shift_type;
DROP TABLE IF EXISTS opening_hours;
DROP TABLE IF EXISTS news;

CREATE TABLE beer (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    style TEXT NOT NULL,
    country_iso_3166_id TEXT NOT NULL,
    abv DECIMAL(2,1) NOT NULL,
    volume_ml INTEGER NOT NULL,
    price_kr INTEGER NOT NULL,
    category_id INTEGER NOT NULL,
    available BOOLEAN NOT NULL,
    FOREIGN KEY (category_id) REFERENCES beer_category (id)
);

CREATE TABLE beer_category (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name_sv TEXT UNIQUE NOT NULL,
    name_en TEXT UNIQUE NOT NULL,
    priority INTEGER NOT NULL
);

CREATE TABLE food (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    price_kr INTEGER NOT NULL,
    available BOOLEAN NOT NULL
);

CREATE TABLE snack (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    price_kr INTEGER NOT NULL,
    available BOOLEAN NOT NULL
);

CREATE TABLE worker (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    display_name TEXT UNIQUE NOT NULL,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    telephone TEXT,
    email TEXT NOT NULL,
    address TEXT,
    note TEXT,
    status_id INTEGER NOT NULL,
    FOREIGN KEY (status_id) REFERENCES worker_status (id)
);

CREATE TABLE worker_status (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
);

CREATE TABLE shift (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    worker_id INTEGER NOT NULL,
    shift_type_id INTEGER NOT NULL,
    date TEXT NOT NULL,
    start TEXT NOT NULL,
    end TEXT NOT NULL,
    FOREIGN KEY (worker_id) REFERENCES worker (id)
    FOREIGN KEY (shift_type_id) REFERENCES shift_type (id)
);

CREATE TABLE shift_type (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

CREATE TABLE opening_hours (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    start TEXT,
    end TEXT
);

CREATE TABLE news (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    time TEXT NOT NULL,
    title_en TEXT NOT NULL,
    body_en TEXT NOT NULL,
    title_sv TEXT NOT NULL,
    body_sv TEXT NOT NULL
);
