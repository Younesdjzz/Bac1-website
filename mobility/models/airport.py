from mobility.db import get_db

def get_airports():
    airports = [{"iata":"LGG", "name":"Liege Airport"},
                {"iata":"BRU", "name":"Bruxelles"}]
    return airports

def get_airport_list():
   db = get_db()
   return db.execute('SELECT * FROM airport ORDER BY iata_code').fetchall()

def search_airport_by_iata_code(iata_code: str):
  # Retourne la ligne correspondant à l'aéroport portant le code iata "iata_code"
    db = get_db()
    return db.execute('SELECT * FROM airport WHERE iata_code=?',(iata_code,)).fetchall() 

class Airport:

   def __init__(self, iata_code, name, iso_country):
      # Constructeur de la classe
      self.iata_code = iata_code
      self.name = name
      self.iso_country = iso_country

   def delete(self):
      # Retire l'aéroport de la DB
      db = get_db()
      db.execute("DELETE FROM airport WHERE iata_code=?",(self.iata_code,))
      db.commit()
   

   def save(self):
      # Sauvegarde l'aéroport dans la DB
        db = get_db()
        db.execute("INSERT INTO airport(iata_code,name, iso_country ) VALUES(?,?,?)",(self.iata_code,self.name,self.iso_country))
        db.commit()

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