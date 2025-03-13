from mobility.db import get_db

def get_airports_list():
    db = get_db()
    return db.execute("SELECT name FROM airport WHERE name IS NOT NULL ORDER BY name ASC").fetchall()

def search_airport_by_iata_code(iata_code: str):
  # Retourne la ligne correspondant à l'aéroport portant le code iata "iata_code"
    db = get_db()
    return db.execute('SELECT * FROM airport WHERE iata_code=?',(iata_code,)).fetchall() 
# Nombre de vols par type d’appareil:
def nombre_de_vols_par_type():
    db=get_db()
    return db.execute("""SELECT aircraft.name, COUNT(*) AS total_vols
                       FROM flight
                       JOIN aircraft ON flight.iata_aircraft = aircraft.iata_aircraft
                       WHERE flight.iata_departure = ?
                       GROUP BY aircraft.name""").fetchall()
# Nombre de vols par jour de la semaine:
def nombre_de_vols_par_jour():
    db=get_db()
    return db.execute("""SELECT strftime('%w', flight.flight_date) AS jour, COUNT(*) AS total_vols
                      FROM flight
                      WHERE flight.iata_departure = ?
                      GROUP BY jour""").fetchall()

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
    