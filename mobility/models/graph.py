from mobility.db import get_db

def aeroport_bel_info(iata_code): 
    db = get_db()
    
    return db.execute("""SELECT 
                      dep_airport.name AS "aeroport_dep",
                      dep_airport.latitude_deg AS "lat_dep", 
                      dep_airport.longitude_deg AS "lon_dep",
                      arr_airport.name AS "Aeroport_arr",
                      arr_airport.latitude_deg AS "Lat_arr",
                      arr_airport.longitude_deg AS "Lon_arr",
                      aircraft.aircraft_type AS "Type_app"
                        FROM flight
                        JOIN airport AS dep_airport ON flight.iata_departure = dep_airport.iata_code
                        JOIN airport AS arr_airport ON flight.iata_arrival = arr_airport.iata_code
                        JOIN aircraft ON flight.iata_aircraft = aircraft.iata_aircraft
                        WHERE dep_airport.iata_code = ?
                        ;""",(iata_code,)).fetchall()

