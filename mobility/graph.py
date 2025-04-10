from flask import (
    Blueprint, render_template, current_app
)

from mobility.db import get_db

from decimal import Decimal
import math
from enum import Enum
from mobility.models.graph import aeroport_bel_info

bp = Blueprint('emission', __name__)

def get_flights():
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
        

class AirCraft(Enum):
    S = 0   #1T
    M = 1   #2.5T
    H = 2   #5T
    J = 3   #12T
    Erreur = 4
    
def distance(lat_from: Decimal, long_from: Decimal,  lat_to: Decimal, long_to: Decimal) -> Decimal:
    ''' Pré: cette fonction prend en arguments, les latitudes et les longitudes des aéroports
        de départ et de destionation. 
        Post: Cette fonction va retourner la distance entre 2 points en km
    '''
    R = 6378

    D = R*(math.acos(math.sin(math.radians(lat_from))*math.sin(math.radians(lat_to))+math.cos(math.radians(lat_from))*math.cos(math.radians(lat_to))*(math.cos(math.radians(long_from)-math.radians(long_to)))))
    return D

def emission(distance: Decimal, aircraft: AirCraft) -> Decimal:
    ''' Pré: cette fonction prend en argument la distance et le type d'appareil qui est un objet de 
        la classe AirCraft 
        Post: cette fonction retourne l'émission de CO2 en kg
    '''
    #condition pour définir la consommation par type d'appareil
    if aircraft == AirCraft.S:
        conso = 1
    elif aircraft == AirCraft.M:
        conso = 2.5
    elif aircraft == AirCraft.H:
        conso = 5
    elif aircraft == AirCraft.J:
        conso = 12
    else: 
        conso = 0
    
    #calcul de la durée de vol
    duree = distance/800

    #calcul de la qtt de CO2 émit
    CO2_emit = conso*3.15*2*duree
    
    return CO2_emit

@bp.route('/voyages')
def page_emission():
    ''' Pré: Cette fonction ne prends pas d'argument
        Post: cette fonction renvoie un dictionnaire qui aura pour clés, les aéroports de départ et comme valeurs, 
        une liste qui contient des listes par départ . 
        Le dico peut se représenter comme telle: 
        d = {"a_dep1" : [["a_dep1": a_arr,emission],[a_dep1...], s = somme des émissions],"a_dep2":[[a_dep2,...]]}
    '''
    l = get_flights()
    d = {}
    for i in l:
        if not i:
            continue  
        a_dep = i[0][0]  
        if a_dep not in d:
            d[a_dep] = []
        for j in i:
            s = 0 
            if j[6] in ["M","S","J","H"]:
                aircraft = AirCraft[j[6]]
            else:
                aircraft = AirCraft[4]
            emission = emission(distance(j[1],j[2],j[4],j[5]), aircraft)
            d[a_dep].append([j[0], j[3],emission])
            #j[0] = a_dep, j[1]=lat_dep, j[2]=long_dep, j[3]=a_arr,j[4]=lat_arr,j[5]=long_arr, j[6]=type_aircraft
            s += emission
        d[a_dep].append(s)

    return render_template("graph.html", data=d)

