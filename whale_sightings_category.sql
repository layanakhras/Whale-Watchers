DROP DATABASE IF EXISTS whale_sightings;
CREATE DATABASE IF NOT EXISTS whale_sightings;
USE whale_sightings;

CREATE TABLE IF NOT EXISTS Sightings (
    sighting_id INT AUTO_INCREMENT PRIMARY KEY,
    sighting_date VARCHAR(20), 
    group_size INT,
    latitude DECIMAL(10, 6),
    longitude DECIMAL(10, 6),
    certainty VARCHAR(50),
    category VARCHAR(50),
    mom_calf VARCHAR(50),
    duplicate VARCHAR(10)
);

CREATE TABLE IF NOT EXISTS Location (
    location_id INT AUTO_INCREMENT PRIMARY KEY,
    latitude DECIMAL(10, 6),
    longitude DECIMAL(10, 6)
);

CREATE TABLE IF NOT EXISTS Category (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS Certainty (
    certainty_id INT AUTO_INCREMENT PRIMARY KEY,
    certainty_level VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS GroupSize (
    group_size_id INT AUTO_INCREMENT PRIMARY KEY,
    group_size_value INT
);

