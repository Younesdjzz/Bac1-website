from mobility.db import get_db

def number_data_airline():
    """
    Retourne le nombre total de compagnies aérienne ainsi qu'un dictionnaire associant pour chaque compagnie le nombre de vol effectués
    pré:
        La connexion à la base de donnée doit être établie 
    post:
        La fonction retourne un tuple (total_airlines,d)
        où:
            total_airlines est un entier représentant le nombre total de compagnies aériennes dans la tables 'airlines'
            d est un dictionnaire dont les clés sont les noms des compagnies aeriennes et les valeurs sont des entiers indiquant le nombre de vol associés à chaque compagnie 

    """
    db = get_db()
    d = {}
    rows = db.execute("SELECT airline.name as name, count(*) as count FROM flight JOIN airline ON flight.iata_airline = airline.iata_airline GROUP BY airline.name ORDER BY count DESC")
    for row in rows:
        if row["name"] is not None:
            d[row["name"]] = row["count"]
            
    
    total_airlines = db.execute("SELECT count(*) FROM airline ").fetchone()[0]
    return total_airlines,d

def number_data_airport():
    """
    Retourne le nombre d'aéroport dans la table airport 
    pré:
        La connexion à la base de donnée doit être établie 
    post:
        number_data_airport() doit retournée un entier correspondant aux nombre d'aéroport total
    """
    db = get_db()
    return db.execute("SELECT count(*) FROM airport ").fetchone()[0]

def number_data_country():
    """
    La fonction retourne le nombre de pays dans la table airport 
    pré:
        La connexion à la base de donné doit être établie
    post:
        number_data_country() retourne un entier correspondant aux nombre total de pays 
    """
    db = get_db()
    return db.execute("SELECT count(*) FROM country ").fetchone()[0]

def number_data_aircraft():
    """
    La fonction retourne le nombre d'avion dans la table aircraft
    pré:
        La connexion à la base de donné doit être établie 
    post:
        number_data_aircraft() retourne un entier correspondant au nombre d'avions total
    """
    db = get_db()
    return db.execute("SELECT count(*) FROM aircraft ").fetchone()[0]

def number_data_flight():
    """
    Retourne le nombre total de vols ainsi qu'un dictionnaire associant le nom de l'aéroport de départ
    au nombre de vols correspondants.
    pré:
        La connexion à la base de donné doit être établie 
    post:
        La fonction retourne un tuple (total_flights, d) 
        où :
            total_flights est un entier indiquant le nombre total de vols.
            d est un dictionnaire dont les clés sont des chaînes représentant les noms des aéroports (non None)
    """
    db = get_db()
    d = {}
    rows = db.execute("SELECT airport.name, count(*) AS count FROM flight JOIN airport ON flight.iata_departure = airport.iata_code GROUP by airport.name ORDER BY count DESC")
    for row in rows:
        if row["name"] is not None:
            d[row["name"]] = row["count"]

    total_flights = db.execute("SELECT count(*) FROM flight ").fetchone()[0]

    return total_flights, d


