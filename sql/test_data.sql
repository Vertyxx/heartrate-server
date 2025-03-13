-- Vložení testovacího pacienta
INSERT INTO Pacient (datum_narozeni, jmeno, prijmeni, narodnost, titul, email, heslo, telefon)
VALUES 
('1990-05-15', 'Jan', 'Novák', 'Česká', 'Bc.', 'jan.novak@example.com', 'heslo123', '+420123456789');

-- Vložení testovacího lékaře
INSERT INTO Lekar (datum_narozeni, jmeno, prijmeni, narodnost, zamereni, email, heslo, telefon)
VALUES 
('1980-03-22', 'Petr', 'Svoboda', 'Česká', 'Kardiologie', 'petr.svoboda@example.com', 'tajneheslo', '+420987654321');

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
