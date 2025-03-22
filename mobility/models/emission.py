from mobility.db import get_db

def aeroport_info(iata_code):
    """Retourne les informations des vols partant d'un aéroport donné."""
    db = get_db()
    result = db.execute("""
        SELECT 
            dep_airport.name AS "Aéroport de départ",
            arr_airport.name AS "Aéroport d'arrivée",
            arr_airport.latitude_deg AS "Latitude arrivée",
            arr_airport.longitude_deg AS "Longitude arrivée",
            aircraft.aircraft_type AS "Type d'appareil"
        FROM flight
        JOIN airport AS dep_airport ON flight.iata_departure = dep_airport.iata_code
        JOIN airport AS arr_airport ON flight.iata_arrival = arr_airport.iata_code
        JOIN aircraft ON flight.iata_aircraft = aircraft.iata_aircraft
        WHERE dep_airport.iata_code = ?;
    """, (iata_code,)).fetchall()  
    
    return result
flights_from_bru = aeroport_info("BRU")
flights_from_crl = aeroport_info("CRL")
flights_from_lgg = aeroport_info("LGG")
flights_from_ost = aeroport_info("OST")
flights_from_anr = aeroport_info("ANR")