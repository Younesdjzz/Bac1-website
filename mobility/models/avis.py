from mobility.db import get_db

def inserer_avis(prenom, entete, message, note, photo_profil):
    db = get_db()
    db.execute("""
        INSERT INTO avis (prenom, entete, message, note, photo_profil)
        VALUES (?, ?, ?, ?, ?)
    """, (prenom, entete, message, note, photo_profil))
    db.commit()
