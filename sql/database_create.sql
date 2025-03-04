CREATE DATABASE HeartRate;
USE HeartRate;

-- Tabulka Pacient
CREATE TABLE Pacient (
    id INT AUTO_INCREMENT PRIMARY KEY,
    datum_narozeni DATE NOT NULL,
    jmeno VARCHAR(50) NOT NULL,
    prijmeni VARCHAR(50) NOT NULL,
    narodnost VARCHAR(50) NOT NULL,
    titul VARCHAR(20), 
    email VARCHAR(100) NOT NULL UNIQUE,
    heslo VARCHAR(100) NOT NULL, 
    telefon VARCHAR(20)
);

-- Tabulka Lekar
CREATE TABLE Lekar (
    id INT AUTO_INCREMENT PRIMARY KEY,
    datum_narozeni DATE NOT NULL,
    jmeno VARCHAR(50) NOT NULL,
    prijmeni VARCHAR(50) NOT NULL,
    narodnost VARCHAR(50) NOT NULL,
    zamereni VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    heslo VARCHAR(100) NOT NULL,        -- Zatím nehashovano
    telefon VARCHAR(20)
);

-- Tabulka pro relaci mezi pacienty a lékaři (mnoho na mnoho)
CREATE TABLE Pacient_Lekar (
    pacient_id INT,
    lekar_id INT,
    PRIMARY KEY (pacient_id, lekar_id),
    FOREIGN KEY (pacient_id) REFERENCES Pacient(id) ON DELETE CASCADE,
    FOREIGN KEY (lekar_id) REFERENCES Lekar(id) ON DELETE CASCADE
);

-- Tabulka Srdecni_aktivita
CREATE TABLE Srdecni_aktivita (
    pacient_id INT NOT NULL,
    cas DATETIME NOT NULL,
    cviceni INT DEFAULT 0 NOT NULL CHECK (cviceni BETWEEN 0 AND 3),
    bpm FLOAT NOT NULL,       -- Nevím jaký datový typ
    PRIMARY KEY (pacient_id, cas),
    FOREIGN KEY (pacient_id) REFERENCES Pacient(id) ON DELETE CASCADE
);