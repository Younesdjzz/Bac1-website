from mobility.db import get_db

def get_country_list():
    db = get_db()
    return db.execute('SELECT * FROM country ORDER BY iso_country').fetchall()

def search_by_iso(iso_country: int):
    db = get_db()
    return db.execute('SELECT * FROM country WHERE iso_country=?', (iso_country,)).fetchall()


class Country:

    def __init__(self, name, iso_country):
        self.name = name
        self.iso_country = iso_country


    @staticmethod
    def get(iso_country: int):
        db = get_db()
        data = db.execute(
            'SELECT * FROM country WHERE iso_country=?', (iso_country,)).fetchone()

        if data is None:
            return None
        else:
            return Country(data["name"], data["iso_country"])