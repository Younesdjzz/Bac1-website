from enum import Enum
import math
from decimal import Decimal

class AirCraft(Enum):
    L = 0
    M = 1
    H = 2
    J = 3

def distance(lat_from: Decimal, long_from: Decimal,  lat_to: Decimal, long_to: Decimal) -> Decimal:
    return 0

def emission(distance: Decimal, aircraft: AirCraft) -> Decimal:
<<<<<<< HEAD
    return 0

def vols_depart_5_aeroports(iata_codes):
    """
    Cette fonction retourne les informations sur tous les vols partant des 5 plus grands aéroports belges
    le 1er janvier 2025.
    
    Pré:
        iata_codes : une liste de 5 codes IATA des aéroports (BRU, CRL, LGG, OST, ANR).
        La connexion avec la base de données doit être établie.
    
    Post:
        La fonction retourne une liste de tuples, chaque tuple contenant les informations suivantes :
        (flight_id, iata_flight, flight_date, iata_departure, departure_airport, 
         iata_arrival, arrival_airport, departure_time, arrival_time, airline, aircraft)
    """
    db = get_db()  
    vols = db.execute("""
        SELECT f.flight_id, f.iata_flight, f.flight_date, 
               f.iata_departure, a1.name AS departure_airport, 
               f.iata_arrival, a2.name AS arrival_airport, 
               f.departure_time, f.arrival_time, 
               al.name AS airline, ac.name AS aircraft
        FROM flight f
        JOIN airport a1 ON f.iata_departure = a1.iata_code
        JOIN airport a2 ON f.iata_arrival = a2.iata_code
        JOIN airline al ON f.iata_airline = al.iata_airline
        JOIN aircraft ac ON f.iata_aircraft = ac.iata_aircraft
        WHERE f.iata_departure IN ('BRU','CRL','LGG','OST','ANR')
          AND f.flight_date = '2025-01-01'
    """, tuple(iata_codes)).fetchall()
    
    return vols
=======
    return 0
>>>>>>> 205f983a9fa8e0c12ccdb7472325fbecb59d3f7c
