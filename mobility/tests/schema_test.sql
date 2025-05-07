PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;

-- Supprimer les tables si elles existent pour éviter les conflits
DROP TABLE IF EXISTS flight;
DROP TABLE IF EXISTS airport;
DROP TABLE IF EXISTS country;
DROP TABLE IF EXISTS airline;
DROP TABLE IF EXISTS aircraft;

-- Table des pays
CREATE TABLE country (
    iso_country TEXT PRIMARY KEY,
    name TEXT NOT NULL
);

-- Table des aéroports
CREATE TABLE airport (
    iata_code TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    latitude_deg REAL,
    longitude_deg REAL,
    iso_country TEXT NOT NULL,
    FOREIGN KEY (iso_country) REFERENCES country(iso_country) ON DELETE CASCADE
);

-- Table des compagnies aériennes
CREATE TABLE airline (
    iata_airline TEXT PRIMARY KEY,
    name TEXT NOT NULL
);

-- Table des types d’aéronefs
CREATE TABLE aircraft (
    iata_aircraft TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    aircraft_type TEXT NOT NULL
);


-- Table des vols
CREATE TABLE flight (
    flight_id INTEGER PRIMARY KEY AUTOINCREMENT,
    iata_airline TEXT NOT NULL,
    iata_aircraft TEXT NOT NULL,
    iata_flight TEXT NOT NULL,
    flight_date TEXT NOT NULL,
    iata_departure TEXT NOT NULL,
    iata_arrival TEXT NOT NULL,
    departure_time TEXT NOT NULL,
    departure_delay INTEGER DEFAULT 0,
    arrival_time TEXT NOT NULL,
    arrival_delay INTEGER DEFAULT 0,
    UNIQUE (flight_date, iata_departure, iata_arrival, departure_time, arrival_time),
    FOREIGN KEY (iata_airline) REFERENCES airline(iata_airline) ON DELETE CASCADE,
    FOREIGN KEY (iata_aircraft) REFERENCES aircraft(iata_aircraft) ON DELETE CASCADE,
    FOREIGN KEY (iata_departure) REFERENCES airport(iata_code) ON DELETE CASCADE,
    FOREIGN KEY (iata_arrival) REFERENCES airport(iata_code) ON DELETE CASCADE
);

-- Aéroports

INSERT INTO airport VALUES ("CRL", "Brussels-South Charleroi", 50.4594, 4.4539, "BE");

-- Compagnies aériennes
INSERT INTO airline VALUES ("AF", "Air France");
INSERT INTO airline VALUES ("AY", "Finnair");
INSERT INTO airline (iata_airline, name) VALUES ('ZZ', 'Test Airline');

-- Types d’aéronefs
INSERT INTO aircraft VALUES ("A320", "Airbus A320", "Jet");
INSERT INTO aircraft VALUES ("E190", "Embraer 190", "Jet");

-- Vols
INSERT INTO flight (
    iata_airline, iata_aircraft, iata_flight, flight_date,
    iata_departure, iata_arrival, departure_time, arrival_time
) VALUES 
("AF", "A320", "AF123", "2025-03-26", "CDG", "CRL", "08:00", "11:00"),
("AY", "E190", "AY456", "2025-03-26", "CRL", "CDG", "13:00", "16:00"),
('ZZ', 'A320', 'ZZ001', '2024-01-15', 'BRU', 'CDG', '10:00', '12:00');

INSERT INTO country (iso_country, name)
VALUES ('BE', 'Belgium'), ('FR', 'France');

INSERT INTO airport (iata_code, name, latitude_deg, longitude_deg, iso_country)
VALUES 
    ('BRU', 'Brussels Airport', 50.9014, 4.4844, 'BE'),
    ('CDG', 'Charles de Gaulle', 49.0097, 2.5479, 'FR');

CREATE TABLE avis (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                prenom TEXT NOT NULL,
                entete TEXT NOT NULL,
                message TEXT NOT NULL,
                note INTEGER NOT NULL,
                photo_profil TEXT
            );

COMMIT;
