from flask import (
    Blueprint, render_template, current_app
)

from mobility.models.graph import aeroport_bel_info
from mobility.emission import *

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
    with current_app.app_context():
         
            l = [aeroport_bel_info("BRU"),aeroport_bel_info("CRL"),aeroport_bel_info("LGG"),aeroport_bel_info("OST"),aeroport_bel_info("ANR")]
    return l

@bp.route('/graphiques')
def page_graphique():
    ''' Pré: Cette fonction ne prends pas d'argument
        Post: cette fonction renvoie un dictionnaire qui aura pour clés, les aéroports de départ et comme valeurs, 
        une liste qui contient des listes par départ . 
        Le dico peut se représenter comme telle: 
        d = {"a_dep1" : [["a_dep1": a_arr,emission],[a_dep1...], s = somme des émissions],"a_dep2":[[a_dep2,...]]}
    '''
    l = get_all_flights()
    liste_aeroport = []
    emission_total = []
    for i in l:
        s = 0 
        if not i:
            continue  
        aeroport = i[0][0] 
        for j in i:
            if j[6] in ["M","S","J","H"]:
                aircraft = AirCraft[j[6]]
            else:
                aircraft = AirCraft[4]
            co2 = emission(distance(j[1],j[2],j[4],j[5]), aircraft)
            s += co2
        emission_total.append(s)
        liste_aeroport.append(aeroport)

    return render_template("graph.html", data=[liste_aeroport, emission_total])

