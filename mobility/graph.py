from flask import (
    Blueprint, redirect, render_template, request, url_for
)


from mobility.models.graph import aeroport_bel_info, flight_world_info, get_all_airports
from mobility.emission import emission, distance, AirCraft


bp = Blueprint('graph', __name__)


def get_all_flights():
    """ Récupère les vols depuis la base de données dans le contexte Flask
        Pré: cette fonction ne prends pas d'arguments
        Post: cette fonction renvoie une liste de 3 niveaux: 
        - premier niveau: liste qui contient toutes les listes
        - deuxième niveau: liste par a_dep. donc 5 dans notre cas
        - troisième niveau: liste par vols ;
        => un vol = [a_dep1, lat_dep, long_dep,a_arr,lat_arr,long_arr,type d'appareil (ex: "M")]
    """

    l = [aeroport_bel_info("BRU"), aeroport_bel_info("CRL"), aeroport_bel_info(
        "LGG"), aeroport_bel_info("OST"), aeroport_bel_info("ANR")]
    return l


@bp.route('/graphiques', methods=['GET'])
def page_graphique():
    '''
    Pré: Cette fonction peut être appelée avec ou sans paramètres GET :
         - sans paramètres : vue globale
         - avec ?dep=XXX&date_deb=YYYY-MM-DD&date_fin=YYYY-MM-DD : vue filtrée
    Post: renvoie les données nécessaires à l'affichage graphique
    '''
    # --- Partie de l'ancienne route `/graphiques`
    liste_des_aeroports = get_all_flights()
    airports = get_all_airports()
    liste_aeroport = []
    emission_total = []

    for aeroport_de_depart in liste_des_aeroports:
        s = 0
        if not aeroport_de_depart:
            continue
        aeroport = aeroport_de_depart[0][0]
        for vols_par_aéroport in aeroport_de_depart:
            if vols_par_aéroport[6] in ["M", "S", "J", "H"]:
                aircraft = AirCraft[vols_par_aéroport[6]]
            else:
                aircraft = AirCraft["M"]
            co2 = emission(distance(
                vols_par_aéroport[1], vols_par_aéroport[2], vols_par_aéroport[4], vols_par_aéroport[5]), aircraft)
            s += co2
        emission_total.append(s)
        liste_aeroport.append(aeroport)

    data = {
        "aeroports": liste_aeroport,
        "emissions": emission_total
    }
    airport_dep = request.args.get('dep')
    date_deb = request.args.get('date_deb')
    date_fin = request.args.get('date_fin')

    if airport_dep and date_deb and date_fin:
        # --- Partie de l'ancienne route `/graphiques/emission`
        resultats = flight_world_info(airport_dep, date_deb, date_fin)
        total_emissions = 0
        emission_par_aéroport = {}

        for vol in resultats:
            if vol[8] not in emission_par_aéroport:
                emission_par_aéroport[vol[8]] = [0]

            lat_from = vol[5]
            lon_from = vol[6]
            lat_to = vol[11]
            lon_to = vol[12]
            type_app = vol[13]

            if not type_app or type_app not in ["M", "S", "J", "H"]:
                aircraft = AirCraft["M"]
            else:
                aircraft = AirCraft[type_app]

            CO2 = emission(distance(lat_from, lon_from,
                           lat_to, lon_to), aircraft)
            emission_par_aéroport[vol[8]][0] += CO2
            total_emissions += CO2

        for pays, liste in emission_par_aéroport.items():
            emission_par_aéroport[pays].append(
                (liste[0] / total_emissions) * 100)

        return render_template("graph.html", data=data, datas=emission_par_aéroport, airports=airports, total_emissions=total_emissions, choix_aeroport=airport_dep)

    return render_template("graph.html", data=data, airports=airports)
