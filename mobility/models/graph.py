from mobility.db import get_db

def aeroport_bel_info(iata_code): 
    db = get_db()
    
    resultats = db.execute("""SELECT 
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
    
    return resultats

def flight_world_info(airport_dep,date_deb,date_fin): 
    db = get_db()
    
    resultats = db.execute("""
    SELECT 
                      
	flight.flight_date as date,
    dep_airport.iso_country AS country_dep,
    dep_country.name AS dep_country_name,
    flight.iata_departure AS iata_dep,
	dep_airport.name AS dep_airport_name,
    dep_airport.latitude_deg AS lat_dep, 
    dep_airport.longitude_deg AS lon_dep,
	
	

    arr_airport.iso_country AS country_arr,
    arr_country.name AS arr_country_name,
    flight.iata_arrival AS iata_arr,
	arr_airport.name AS arr_airport_name,
    arr_airport.latitude_deg AS lat_arr,
    arr_airport.longitude_deg AS lon_arr,

    aircraft.aircraft_type AS type_app

    FROM flight
    JOIN airport AS dep_airport ON flight.iata_departure = dep_airport.iata_code
    JOIN airport AS arr_airport ON flight.iata_arrival = arr_airport.iata_code
    JOIN country AS dep_country ON dep_airport.iso_country = dep_country.iso_country
    JOIN country AS arr_country ON arr_airport.iso_country = arr_country.iso_country


    JOIN aircraft ON flight.iata_aircraft = aircraft.iata_aircraft
	WHERE dep_airport_name = ? 
	AND flight.flight_date BETWEEN ? AND ?

    ORDER BY dep_airport.iso_country
    ;
    """, (airport_dep, date_deb, date_fin)).fetchall()
    
    return resultats

def get_all_airports():
    """
    Cette fonction s'ocuppe de prendre le nom des aeroports dans la base de donnée 
    pré: la connexion avec la base de donnée doit être établie 
    post:La fonction retourne une liste des noms d'aeroport
    """

    db = get_db()
    return db.execute("SELECT name FROM airport WHERE name IS NOT NULL ORDER BY name ASC").fetchall()

