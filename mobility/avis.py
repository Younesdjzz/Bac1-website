from flask import (
    Blueprint, render_template, request, redirect, url_for, flash
)
import os

bp = Blueprint('avis', __name__)


@bp.route("/avis")
def avis():
    donner_etoiles = []  # Les possibilités, de 1 jusqu'à 5 étoiles
    for nbr in range(1, 6):
        donner_etoiles.append(["star" + str(nbr), str(nbr)])

    # Lister les fichiers dans le dossier uploads
    images = []
    chemin_uploads = os.path.join('mobility/static/uploads')
    for f in os.listdir(chemin_uploads):
        images.append(f)

    return render_template("avis.html", donner_etoiles=donner_etoiles, images=images)

# Vue pour gérer l'envoi
@bp.route("/envoyer_avis", methods=["POST"])
def envoyer_avis():
    note = request.form.get("note")
    prenom = request.form.get("prenom")
    entete = request.form.get("entete")
    message = request.form.get("message")
    photo_profil = request.form.get("photo_profil")

    # ici : code pour les enregistrer dans la base SQL :
    # (note, entete, message, photo_profil)

    flash("Avis envoyé avec succès !", "success")
    return redirect(url_for("avis"))
