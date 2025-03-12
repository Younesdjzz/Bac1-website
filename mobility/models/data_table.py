from mobility.db import get_db

def number_data_airline():
    db = get_db()
    d = {}
    rows = db.execute("SELECT airline.name as name, count(*) as count FROM flight JOIN airline ON flight.iata_airline = airline.iata_airline GROUP BY airline.name")
    for row in rows:
        if row["name"] is not None:
            d[row["name"]] = row["count"]
            
    
    total_airlines = db.execute("SELECT count(*) FROM airline ").fetchone()[0]
    return total_airlines,d

def number_data_airport():
    db = get_db()
    return db.execute("SELECT count(*) FROM airport ").fetchone()[0]

def number_data_country():
    db = get_db()
    return db.execute("SELECT count(*) FROM country ").fetchone()[0]

def number_data_aircraft():
    db = get_db()
    return db.execute("SELECT count(*) FROM aircraft ").fetchone()[0]

def number_data_flight():
    db = get_db()
    d = {}
    rows = db.execute("SELECT airport.name, count(*) AS count FROM flight JOIN airport ON flight.iata_departure = airport.iata_code GROUP by airport.name")
    for row in rows:
        if row["name"] is not None:
            d[row["name"]] = row["count"]

    total_flights = db.execute("SELECT count(*) FROM flight ").fetchone()[0]

    return total_flights, d

