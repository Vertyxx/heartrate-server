-- Vložení testovacího pacienta
    -- Heslo: heslo123
INSERT INTO Pacient (datum_narozeni, jmeno, prijmeni, narodnost, titul, email, heslo, telefon)
VALUES 
('1990-05-15', 'Jan', 'Novák', 'Česká', 'Bc.', 'jan.novak@example.com', 'pbkdf2:sha256:1000000$Qlf17t9cYnbeLdhH$7115bc786ba45a0b8799243a92964e8695caffea120f0553f25576b1544355f5', '+420123456789');

-- Vložení testovacího lékaře
    -- Heslo: tajneheslo
INSERT INTO Lekar (datum_narozeni, jmeno, prijmeni, narodnost, zamereni, email, heslo, telefon)
VALUES 
('1980-03-22', 'Petr', 'Svoboda', 'Česká', 'Kardiologie', 'petr.svoboda@example.com', 'pbkdf2:sha256:1000000$bGrfhvtKDUsItA25$30f7650aebfbf9247f5c301a99d794aa49b53690f81326ee9ec0646dd26650ff', '+420987654321');

-- Přiřazení pacienta k lékaři (potřebujeme ID)
INSERT INTO Pacient_Lekar (pacient_id, lekar_id, stav)
VALUES 
((SELECT id FROM Pacient WHERE email = 'jan.novak@example.com'), 
 (SELECT id FROM Lekar WHERE email = 'petr.svoboda@example.com'),
 1);

-- Vložení testovací srdeční aktivity pro pacienta
INSERT INTO Srdecni_aktivita (pacient_id, cas, cviceni, bpm)
VALUES 
((SELECT id FROM Pacient WHERE email = 'jan.novak@example.com'), NOW(), 0, 60.5);
