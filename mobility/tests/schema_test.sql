PRAGMA foreign_keys=ON;  
BEGIN TRANSACTION;


DROP TABLE IF EXISTS vols;
DROP TABLE IF EXISTS airport;
DROP TABLE IF EXISTS country;


CREATE TABLE country (
    iso_country TEXT PRIMARY KEY,  
    name TEXT NOT NULL             
);


CREATE TABLE airport (
    iata_code TEXT PRIMARY KEY,   
    name TEXT NOT NULL,           
    iso_country TEXT NOT NULL,    
    FOREIGN KEY (iso_country) REFERENCES country(iso_country)  
);

CREATE TABLE vols (
    id INTEGER PRIMARY KEY AUTOINCREMENT,       
    airport_depart TEXT NOT NULL,              
    airport_arrivee TEXT NOT NULL,             
    heure_vol TEXT NOT NULL,                   
    type_avion TEXT,                           
    est_cargo BOOLEAN NOT NULL CHECK (est_cargo IN (0,1)),  
    FOREIGN KEY (airport_depart) REFERENCES airport(iata_code),  
    FOREIGN KEY (airport_arrivee) REFERENCES airport(iata_code)  
);


INSERT INTO country (iso_country, name) VALUES
('BE', 'Belgique'),
('FR', 'France'),
('US', 'United States');


INSERT INTO airport (iata_code, name, iso_country) VALUES
('BRU', 'Aéroport de Bruxelles', 'BE'),
('CRL', 'Aéroport de Charleroi', 'BE'),
('LGG', 'Aéroport de Liège', 'BE');


INSERT INTO airport (iata_code, name, iso_country) VALUES
('ENF', 'Enontekio Airport', 'FI');


INSERT INTO vols (airport_depart, airport_arrivee, heure_vol, type_avion, est_cargo) VALUES
('BRU', 'LGG', '2024-03-01 08:00:00', 'Boeing 747', 0),
('CRL', 'BRU', '2024-03-01 10:30:00', 'Airbus A320', 0),
('LGG', 'BRU', '2024-03-02 14:00:00', 'Boeing 777', 1);

COMMIT;