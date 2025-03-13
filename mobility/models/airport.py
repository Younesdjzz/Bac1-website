from mobility.db import get_db

def get_all_airports():
    db = get_db()
    return db.execute("SELECT name FROM airport WHERE name IS NOT NULL ORDER BY name ASC").fetchall()

def search_airport_by_iata_code(iata_code: str):
  # Retourne la ligne correspondant à l'aéroport portant le code iata "iata_code"
    db = get_db()
    return db.execute('SELECT * FROM airport WHERE iata_code=?',(iata_code,)).fetchall() 

# Nombre de vols par type d’appareil:
def nombre_de_vols_par_type(iata_code):
    db=get_db()
    return db.execute("""SELECT aircraft_type, COUNT(*) AS vols_totaux FROM flight
                       INNER JOIN aircraft ON (flight.iata_aircraft = aircraft.iata_aircraft)
                      WHERE (iata_departure = ? OR iata_arrival = ?)
					   GROUP BY aircraft_type""", (iata_code, iata_code)).fetchall()

# Nombre de vols par jour de la semaine:
def nombre_de_vols_par_jour(iata_code):
    db = get_db()

    # Effectuer la requête pour obtenir le nombre de vols par jour
    vols_jour = db.execute("""
        SELECT 
            CASE strftime('%w', flight_date)
                WHEN '0' THEN 'Lundi'
                WHEN '1' THEN 'Mardi'
                WHEN '2' THEN 'Mercredi'
                WHEN '3' THEN 'Jeudi'
                WHEN '4' THEN 'Vendredi'
                WHEN '5' THEN 'Samedi'
                WHEN '6' THEN 'Dimanche'
            END AS jour_semaine,
            COUNT(*) AS nombre_de_vols
        FROM flight
        WHERE flight_date IS NOT NULL
        AND (iata_departure = ? OR iata_arrival = ?)
        GROUP BY jour_semaine
        ORDER BY CAST(strftime('%w', flight_date) AS INTEGER)
    """, (iata_code, iata_code)).fetchall()

    return vols_jour


class Airport:
    
    def __init__(self, iata_code, name, iso_country):
        # Constructeur de la classe
        self.iata_code = iata_code
        self.name = name
        self.iso_country = iso_country


    @staticmethod
    def get(iata_code: str):
        # Retourne un objet Aéroport construit à partir des informations de la DB
        # récupérer à partir du code iata "iata_code"
        # Retourne none si aucun aéroport avec le code iata "iata_code"
        # se trouve dans la DB
        # Vous pouvez vous insprirer de la classe Country implémentée précédemment
        db = get_db()
        data = db.execute(
            'SELECT * FROM airport WHERE iata_code=?', (iata_code,)).fetchone()

        if data is None:
            return None
        else:
            return Airport(data["iata_code"], data["name"], data["iso_country"])
    