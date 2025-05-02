from flask import (
    Blueprint, render_template, request, redirect, url_for, flash
)
import os
from mobility.models.avis import inserer_avis
from mobility.db import get_db

bp = Blueprint('avis', __name__)


@bp.route("/avis")
def avis():
    donner_etoiles = []  # Les possibilités, de 1 jusqu'à 5 étoiles
    for nbr in range(5, 0, -1):
        donner_etoiles.append(["star" + str(nbr), str(nbr)])

    # Lister les fichiers dans le dossier uploads
    images = []
    chemin_uploads = os.path.join('mobility/static/uploads')
    for f in os.listdir(chemin_uploads):
        if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp')) : # Pour corriger le bug du choix "image" (alt)
            images.append(f)

    db = get_db()
    avis_liste = db.execute("SELECT * FROM avis ORDER BY date DESC").fetchall()

    return render_template("avis.html", donner_etoiles=donner_etoiles, images=images, avis_liste=avis_liste  )

# Vue pour gérer l'envoi
@bp.route("/envoyer_avis", methods=["POST"])
def envoyer_avis():
    note = int(request.form.get("note"))
    prenom = request.form.get("prenom")
    entete = request.form.get("entete")
    message = request.form.get("message")
    photo_profil = request.form.get("photo_profil")
    # Insérer l'avis dans la base de données
    inserer_avis(prenom, entete, message, note, photo_profil)



    


    flash("Avis envoyé avec succès !", "success")
    return redirect(url_for("avis.avis"))


@bp.route("/supprimer_avis/<int:avis_id>", methods=["POST"])
def supprimer_avis(avis_id):
    db = get_db()
    db.execute("DELETE FROM avis WHERE id = ?", (avis_id,))
    db.commit()
    flash("Avis supprimé avec succès !", "success")
    return redirect(url_for("avis.avis"))

