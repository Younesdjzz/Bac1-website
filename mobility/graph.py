from flask import (
   Blueprint, redirect, render_template, request, url_for
)


from mobility.models.graph import aeroport_bel_info,flight_world_info,get_all_airports
from mobility.emission import emission,distance,AirCraft


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
    liste_des_aéroports = get_all_flights()
    liste_aeroport = []
    emission_total = []
    for aéroport_de_départ in liste_des_aéroports:
        s = 0 
        if not aéroport_de_départ:
            continue  
        aeroport = aéroport_de_départ[0][0] 
        for vols_par_aéroport in aéroport_de_départ:
            if vols_par_aéroport[6] in ["M","S","J","H"]:
                aircraft = AirCraft[vols_par_aéroport[6]]
            else:
                aircraft = AirCraft["M"]
            co2 = emission(distance(vols_par_aéroport[1],vols_par_aéroport[2],vols_par_aéroport[4],vols_par_aéroport[5]), aircraft)
            s += co2
        emission_total.append(s)
        liste_aeroport.append(aeroport)

    data = {
        "aeroports": liste_aeroport,
        "emissions": emission_total
    }

    return render_template("graph.html", data=data)



@bp.route('/graphiques/emission', methods=['GET'])
def requete_emission():
    airport_dep = request.args.get('dep')
    date_deb = request.args.get('date_deb')
    date_fin = request.args.get('date_fin')

    resultats = flight_world_info(airport_dep, date_deb, date_fin)

    
    airports = get_all_airports()

    total_emissions = 0
    emission_par_aéroport = {}
    for vol in resultats:
        if not vol[8] in emission_par_aéroport:
            emission_par_aéroport[vol[8]]= [0]

      
        lat_from = vol[5]
        lon_from = vol[6]
        lat_to = vol[11]
        lon_to = vol[12]
        type_app = vol[13]

        if not type_app or type_app not in ["M", "S", "J", "H"]:
            aircraft = AirCraft["M"]
        else:
            aircraft = AirCraft[type_app]

        CO2 = emission(distance(lat_from, lon_from, lat_to, lon_to), aircraft)
        emission_par_aéroport[vol[8]][0] += CO2
        total_emissions += CO2
    for pays,liste in emission_par_aéroport.items():

        emission_par_aéroport[pays].append((liste[0]/total_emissions)*100)

    return render_template("graph.html", datas=emission_par_aéroport,airports=airports,total_emissions=total_emissions)
    


