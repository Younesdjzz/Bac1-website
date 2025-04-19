from mobility.db import get_db

def get_all_airports():
    """
    Cette fonction s'ocuppe de prendre le nom des aeroports dans la base de donnée 
    pré: la connexion avec la base de donnée doit être établie 
    post:La fonction retourne une liste des noms d'aeroport
    """

    db = get_db()
    return db.execute("SELECT name FROM airport WHERE name IS NOT NULL ORDER BY name ASC").fetchall()

# Trouver l'iata d'un aeroport:
def get_iata_by_airport_name(airport_name) :
    """
    Pré : airport_name = le nom de l'aeroport
    Post : return l'iata de cet aéroport
    """
    db = get_db()
    return db.execute("SELECT iata_code FROM airport WHERE LOWER(name) = LOWER(?)", (airport_name.lower(),)).fetchone()

def search_airport_by_iata_code(iata_code: str):
    """
    Cette fonction retourne les données de l'aeroport correspondant au IATA code spécifiée
    pré: 
        IAtA code doit être une chaine de carcarctére de longueur len>0
        La connexion avec la base de donnée doit être établie
    post: 
        La fonction retourne une liste
        La fonction doit retournée toutes les informations de l'aeroport correspondant au IATA code 
    """

  # Retourne la ligne correspondant à l'aéroport portant le code iata "iata_code"
    db = get_db()
    return db.execute('SELECT * FROM airport WHERE iata_code=?',(iata_code,)).fetchall() 

# Nombre de vols par type d’appareil:
def nombre_de_vols_par_type(iata_code):
    """
    La fonction retourne le nombre de vol par appareil pour l'aeroport correspondant au IATA code 
    pré: 
        IAtA code doit être une chaine de carcarctére de longueur len>0
        La connexion avec la base de donnée doit être établie
    post:
        La fonction retourne une liste 
        - Chaque élément de la liste est un tuple de la forme (aircraft_type, vols_totaux),
        où :
            aircraft_type est une chaîne de caractères,
            vols_totaux est un entier représentant le nombre de vols.
    """
    db=get_db()
    return db.execute("""SELECT aircraft_type, COUNT(*) AS vols_totaux FROM flight
                       INNER JOIN aircraft ON (flight.iata_aircraft = aircraft.iata_aircraft)
                      WHERE (iata_departure = ? OR iata_arrival = ?)
					   GROUP BY aircraft_type""", (iata_code, iata_code)).fetchall()

# Nombre de vols par jour de la semaine:
def nombre_de_vols_par_jour(iata_code):
    """
    La fonction retourne le nombre de vols de l'aeroport correspondant au IATA code par jour 
    pré: 
        IAtA code doit être une chaine de carcarctére de longueur len>0
        La connexion avec la base de donnée doit être établie
    post: La focntion retourne une liste 
        Chaque élement de la liste est un tuple de la forme (jours_semaine, nombre_de_vols)
        où jours_semaine est une chaine de caractére et nombre_de_vols est un entier
    """
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
    """
    Classe representant un aéroport défini par son IATA code, son nom , et le ISO code du pays
    """
    
    def __init__(self, iata_code, name, iso_country):
        """
        pré:
            iata_code , name, iso_country doivent être des chaines de caractères de longueur len>0
        post:
            Un objet Airport est créé avec les attributs spécifiés.

            iata_code: Code IATA de l'aéroport.
            name: Nom de l'aéroport.
            iso_country: Code ISO du pays de l'aéroport.
            """
        # Constructeur de la classe
        self.iata_code = iata_code
        self.name = name
        self.iso_country = iso_country


    @staticmethod
    def get(iata_code: str):
        """       
        Retourne un objet Airport construit à partir des informations récupérées dans la base de données
        à partir du code IATA fourni. Retourne none si aucun aéroport correspondant n'est trouvé.
        pré:
            iata_code doit être une chaine de caractére de longueur len>0
            La connexion à la base de donnée doit être établie
        post:
            Retourne un objet Airport si un aéroport avec le code IATA existe dans la DB, sinon none.

        """
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
    