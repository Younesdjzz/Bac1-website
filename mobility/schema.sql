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
