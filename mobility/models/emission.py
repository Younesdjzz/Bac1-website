from mobility.db import get_db
from mobility import create_app

app = create_app()

def aeroport_info(iata_code): 
    db = get_db()
    return db.execute("""SELECT dep_airport.name AS "Aeroport de depart",arr_airport.name AS "Aeroport d'arrivee",.latitude_deg AS "Latitude arrivée",arr_airport.longitude_deg AS "Longitude arrivée",aircraft.aircraft_type AS "Type d'appareil"
                        FROM flight
                        JOIN airport AS dep_airport ON flight.iata_departure = dep_airport.iata_code
                        JOIN airport AS arr_airport ON flight.iata_arrival = arr_airport.iata_code
                        JOIN aircraft ON flight.iata_aircraft = aircraft.iata_aircraft
                        WHERE dep_airport.iata_code = ?""",(iata_code, iata_code)).fetchall()


flights_from_bru = aeroport_info("BRU")
flights_from_crl = aeroport_info("CRL")
flights_from_lgg = aeroport_info("LGG")
flights_from_ost = aeroport_info("OST")
flights_from_anr = aeroport_info("ANR")