from flask import (
   Blueprint, redirect, render_template, request, url_for
)

from mobility.models.airport import Airport
from mobility.models.airport import get_all_airports,search_airport_by_iata_code


bp = Blueprint('airport', __name__)

# Define the routes code
@bp.route('/airport')
def airport_list():
   submitted = False
   if request.args.get('airport'):
      submitted = True
   airports = get_all_airports()
   return render_template("airports.html", airports=airports, submitted=submitted)

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