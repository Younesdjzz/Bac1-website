from flask import (
   Blueprint, render_template, request
)

from mobility.db import get_db
from mobility.models.airport import get_all_airports, get_iata_by_airport_name, nombre_de_vols_par_type, nombre_de_vols_par_jour

bp = Blueprint('airport', __name__)

# Define the routes code
@bp.route('/airport', methods=['GET'])
def requete_aeroport():
    """
    Traite la requête HTTP pour rechercher un aéroport par son nom et afficher les informations associées.
    
    pré:
        La connexion à la base de données est établie (get_db() ne doit pas retourner None).
        La fonction request.args.get('airport_name') retourne soit None, soit une chaîne de caractères.
        Les fonctions get_all_airports(), nombre_de_vols_par_jour() et nombre_de_vols_par_type() doivent être définies et fonctionner correctement.

    post:
        La fonction retourne le rendu du template "airports.html" avec les variables suivantes:
            airports: une liste contenant tous les aéroports.
            vols_jour: soit la liste des vols par jour pour l'aéroport trouvé, soit une liste avec des valeurs par défaut (si aucun vol n'est trouvé).
            vols_type: soit la liste des vols par type pour l'aéroport trouvé, soit une liste avec des valeurs par défaut.
            selected_airport: le nom de l'aéroport tel qu'indiqué dans la requête.
            airport_not_found: un booléen indiquant si l'aéroport recherché n'a pas été trouvé dans la base de données.
    """
    db = get_db()
    airport_name = request.args.get('airport_name')

    airports = get_all_airports()
    vols_jour = []
    vols_type = []
    airport_not_found = False 
    if airport_name:
        airport = get_iata_by_airport_name(airport_name)

        if airport:
            iata_code = airport[0]
            vols_jour = nombre_de_vols_par_jour(iata_code)
            vols_type = nombre_de_vols_par_type(iata_code)


        if not airport:
            airport_not_found = True

        elif not vols_jour:
            jours_semaine = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']
            vols_jour = [{'jour_semaine': jour, 'nombre_de_vols': 0} for jour in jours_semaine]
            vols_type = [{'name': "/", 'aircraft_type': "/", 'vols_totaux': "/"}]

    return render_template("airports.html", 
                           airports=airports, 
                           vols_jour=vols_jour, 
                           vols_type=vols_type, 
                           selected_airport=airport_name,
                           airport_not_found=airport_not_found)