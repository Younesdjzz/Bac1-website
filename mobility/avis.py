from flask import (
    Blueprint, render_template
)

bp = Blueprint('avis', __name__)

@bp.route("/avis")
def avis():
    etoiles = []
    for nbr in range(1, 6) : # De 1 jusqu'à 5 étoiles
        etoiles.append(["star" + str(nbr), str(nbr)])

    return render_template("avis.html", etoiles=etoiles)