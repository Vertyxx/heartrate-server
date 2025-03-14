-- CREATE DATABASE HeartRate;
USE HeartRate;

-- Tabulka User (nahrazuje Pacient i Lekar)
CREATE TABLE IF NOT EXISTS User (
    id INT AUTO_INCREMENT PRIMARY KEY,
    datum_narozeni DATE,
    jmeno VARCHAR(50) NOT NULL,
    prijmeni VARCHAR(50) NOT NULL,
    narodnost VARCHAR(50) DEFAULT NULL,
    titul VARCHAR(20) DEFAULT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    heslo VARCHAR(255) NOT NULL, 
    telefon VARCHAR(20) DEFAULT NULL,
    role ENUM('pacient', 'lekar') NOT NULL, -- Určuje, zda je uživatel pacient nebo lékař
    zamereni VARCHAR(100) DEFAULT NULL -- Pouze pro lékaře (pacienti budou mít NULL)
);

-- Tabulka pro relaci mezi uživateli (pacienti & lékaři & lékaři mezi sebou)
    -- stav: 0 = čekající na schválení, 1 = schválený, 2 = zamítnutý, 3 = ukončený
CREATE TABLE IF NOT EXISTS Pacient_Lekar (
    pacient_id INT NOT NULL,
    lekar_id INT NOT NULL,
    stav INT DEFAULT 0 NOT NULL CHECK (stav BETWEEN 0 AND 3), 
    PRIMARY KEY (pacient_id, lekar_id),
    FOREIGN KEY (pacient_id) REFERENCES User(id) ON DELETE CASCADE,
    FOREIGN KEY (lekar_id) REFERENCES User(id) ON DELETE CASCADE
);

-- Tabulka Srdecni_aktivita (může zaznamenávat pacient i lékař)
CREATE TABLE IF NOT EXISTS Srdecni_aktivita (
    uzivatel_id INT NOT NULL,
    cas DATETIME NOT NULL,
    cviceni INT DEFAULT 0 NOT NULL CHECK (cviceni BETWEEN 0 AND 3),
    bpm FLOAT NOT NULL,
    PRIMARY KEY (uzivatel_id, cas),
    FOREIGN KEY (uzivatel_id) REFERENCES User(id) ON DELETE CASCADE
);