from flask import (
    Blueprint, render_template, current_app
)
from mobility.models.emission import aeroport_info
from mobility.db import get_db

from decimal import Decimal
import math
from enum import Enum

bp = Blueprint('emission', __name__)


def get_flights():
    """Récupère les vols depuis la base de données dans le contexte Flask"""
    with current_app.app_context():
         
            l = [aeroport_info("BRU"),aeroport_info("CRL"),aeroport_info("LGG"),aeroport_info("OST"),aeroport_info("ANR")]
    return l
        

class AirCraft(Enum):
    S = 0   #1T
    M = 1   #2.5T
    H = 2   #5T
    J = 3   #12T
    Erreur = 4
    
def distance(lat_from: Decimal, long_from: Decimal,  lat_to: Decimal, long_to: Decimal) -> Decimal:
    '''Cette fonction va retourner la distance entre 2 points'''
    R = 6378

    D = R*(math.acos(math.sin(math.radians(lat_from))*math.sin(math.radians(lat_to))+math.cos(math.radians(lat_from))*math.cos(math.radians(lat_to))*(math.cos(math.radians(long_from)-math.radians(long_to)))))
    return D

def emission(distance: Decimal, aircraft: AirCraft) -> Decimal:
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



@bp.route('/emission')
def page_emission():
    l = get_flights()
    d = {}
    for i in l:
        if not i:
            continue  
        a_dep = i[0][0]  
        if a_dep not in d:
            d[a_dep] = []

        for j in i:
            if j[6] in ["M","S","J","H"]:
                aircraft = AirCraft[j[6]]
            else:
                aircraft = AirCraft[4]
            d[a_dep].append([j[0], j[3],distance(j[1],j[2],j[4],j[5]),emission(distance(j[1],j[2],j[4],j[5]), aircraft) ])
            #j[0] = a_dep, j[1]=lat_dep, j[2]=long_dep, j[3]=a_arr,j[4]=lat_arr,j[5]=long_arr, j[6]=type_aircraft

    return render_template("emission.html", data=d)


