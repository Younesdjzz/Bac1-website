from flask import (
   Blueprint, redirect, render_template, request, url_for
)

from mobility.db import get_db
from mobility.models.airport import Airport
from mobility.models.airport import get_all_airports, nombre_de_vols_par_type, nombre_de_vols_par_jour


bp = Blueprint('airport', __name__)

# Define the routes code
@bp.route('/airport', methods=['GET'])
def requete_aeroport():
    db = get_db()
    airport_name = request.args.get('airport_name')

    airports = get_all_airports()
    vols_type = nombre_de_vols_par_type()
    vols_jour = [] 
    airport_not_found = False 

    if airport_name:
        airport = db.execute("""
            SELECT iata_code FROM airport WHERE LOWER(name) = LOWER(?)
        """, (airport_name.lower(),)).fetchone()

        if airport:
            iata_code = airport[0]
            vols_jour = nombre_de_vols_par_jour(iata_code)

        if not airport:
            airport_not_found = True

        elif not vols_jour:
            jours_semaine = ['Lundi', 'Mardi', 'Mercredi', 'jeudi', 'Vendredi', 'Samedi', 'Dimanche']
            vols_jour = [{'jour_semaine': jour, 'nombre_de_vols': 0} for jour in jours_semaine]

    return render_template("airports.html", 
                           airports=airports, 
                           vols_jour=vols_jour, 
                           vols_type=vols_type, 
                           selected_airport=airport_name,
                           airport_not_found=airport_not_found)

