from flask import (
   Blueprint, redirect, render_template, request, url_for
)

from mobility.models.airport import Airport
from mobility.models.airport import get_airport_list,search_airport_by_iata_code

from mobility.models.airport import get_airports

bp = Blueprint('airport', __name__)

# Define the routes code
@bp.route('/')
def airport_list():
   # Page principal qui affiche la liste des aéroports
   # avec leur nom, code IATA et le nom de leur pays correspondant
   airports = get_airport_list()
   return render_template("airports.html", airports=airports)

@bp.route("/create_airport", methods=["POST"])
def airport_create():
   # Page permettant d'ajouter un aéroport, similaire à "create_country"
    iata_code = request.form["iata_code"]
    if not search_airport_by_iata_code(str(iata_code)):
        print("Creating airport")
        name = request.form["name"]
        iso_country = request.form["iso_country"]
        airport = Airport(iata_code,name,iso_country)
        airport.save()
    return redirect(url_for("country.country_list"))

@bp.route("/delete_airport/<iata_code>")
def airport_delete(iata_code):
   # Page permettant de retirer un aéroport, similaire à "delete_country"
    airport = Airport.get(iata_code)
    if airport:
        airport.delete()
    return redirect(url_for("airport.airport_list"))
