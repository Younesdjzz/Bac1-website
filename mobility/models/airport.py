import sqlite3
def get_airports():
    airports = [{"iata":"LGG", "name":"Liege Airport"},
                {"iata":"BRU", "name":"Bruxelles"}]
    return airports

class Airport:
    def __init__(self, iata_code, name, iso_country):
        self.iata_code = iata_code
        self.name = name
        self.iso_country = iso_country

    def delete(self):
        """Supprime l'aéroport de la base de données."""
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM airport WHERE iata_code = ?", (self.iata_code,))
        conn.commit()
        conn.close()

    def save(self):
        """Enregistre ou met à jour l'aéroport dans la base de données."""
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO airport (iata_code, name, iso_country) 
            VALUES (?, ?, ?)
            ON CONFLICT(iata_code) DO UPDATE SET name = excluded.name, iso_country = excluded.iso_country
        """, (self.iata_code, self.name, self.iso_country))
        conn.commit()
        conn.close()

    @staticmethod
    def get(iata_code: str):
        """Retourne un objet Airport correspondant à l'iata_code donné."""
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT iata_code, name, iso_country FROM airport WHERE iata_code = ?", (iata_code,))
        row = cursor.fetchone()
        conn.close()
        return Airport(*row) if row else None

def get_airport_list():
    """Retourne la liste des aéroports avec le nom du pays, triée par pays."""
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT airport.iata_code, airport.name, country.name 
        FROM airport 
        JOIN country ON airport.iso_country = country.iso_country 
        ORDER BY country.name
    """)
    airports = cursor.fetchall()
    conn.close()
    return airports  

def search_airport_by_iata_code(iata_code: str):
    """Retourne les informations d'un aéroport à partir de son code IATA."""
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM airport WHERE iata_code = ?", (iata_code,))
    airport = cursor.fetchone()
    conn.close()
    return airport  