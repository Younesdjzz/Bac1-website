from flask import (
    Blueprint, render_template, request, redirect, url_for
)
from mobility.models.stats import *

bp = Blueprint('number_data_table', __name__)

@bp.route('/statistiques')
def compute_data():
    """Calcule diverses statistiques sur les vols, compagnies aériennes, aéroports, pays et avions,
    puis retourne le rendu du template "statistique.html" en transmettant ces données."""

    total_flights_airport, flights_by_airport = number_data_flight()
    total_flights_airline, flights_by_airline = number_data_airline()
    data = {
        "airlines": total_flights_airline,
        "flights_by_airline": flights_by_airline,
        "airports": number_data_airport(),
        "countries": number_data_country(),
        "aircrafts": number_data_aircraft(),
        "flights": total_flights_airport,
        "flights_by_airport": flights_by_airport
    }
    return render_template("statistique.html", data=data)



