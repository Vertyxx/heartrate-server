-- Vložení testovacího pacienta
INSERT INTO User (datum_narozeni, jmeno, prijmeni, narodnost, titul, email, heslo, telefon, role, zamereni)
VALUES 
('1990-05-15', 'Jan', 'Novák', 'Česká', 'Bc.', 'jan.novak@example.com', 'pbkdf2:sha256:1000000$Qlf17t9cYnbeLdhH$7115bc786ba45a0b8799243a92964e8695caffea120f0553f25576b1544355f5', '+420123456789', 'pacient', NULL);

-- Vložení testovacího lékaře
INSERT INTO User (datum_narozeni, jmeno, prijmeni, narodnost, titul, email, heslo, telefon, role, zamereni)
VALUES 
('1980-03-22', 'Petr', 'Svoboda', 'Česká', 'MUDr.', 'petr.svoboda@example.com', 'pbkdf2:sha256:1000000$bGrfhvtKDUsItA25$30f7650aebfbf9247f5c301a99d794aa49b53690f81326ee9ec0646dd26650ff', '+420987654321', 'lekar', 'Kardiologie');

-- Přiřazení pacienta k lékaři (výchozí stav: schválený)
INSERT INTO Pacient_Lekar (pacient_id, lekar_id, stav)
VALUES 
((SELECT id FROM User WHERE email = 'jan.novak@example.com'), 
 (SELECT id FROM User WHERE email = 'petr.svoboda@example.com'), 
 1);

-- Vložení testovací srdeční aktivity pro pacienta
INSERT INTO Srdecni_aktivita (uzivatel_id, cas, cviceni, bpm)
VALUES 
((SELECT id FROM User WHERE email = 'jan.novak@example.com'), 
 NOW(), 2, 75.5);

-- Lékař si zaznamenává vlastní srdeční aktivitu
INSERT INTO Srdecni_aktivita (uzivatel_id, cas, cviceni, bpm)
VALUES 
((SELECT id FROM User WHERE email = 'petr.svoboda@example.com'), 
 NOW(), 1, 65.0);
