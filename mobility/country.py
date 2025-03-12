from flask import (
    Blueprint, render_template, request, redirect, url_for
)
from mobility.models.country import get_country_list, search_by_iso, Country

bp = Blueprint('country', __name__)


# route code
@bp.route('/country')
def country_list():
    countries = get_country_list()
    return render_template("country.html", countries=countries)

@bp.route("/create_country", methods=["POST"])
def country_create():
    iso_country = request.form["iso_country"]
    if not search_by_iso(str(iso_country)):
        print("Creating country")
        name = request.form["name"]
        country = Country(name, iso_country)
        country.save()
    print("Country already exists")
    return redirect(url_for("country.country_list"))


@bp.route("/delete_country/<iso_country>")
def country_delete(iso_country):
    country = Country.get(iso_country)
    if country:
        country.delete()
    return redirect(url_for("country.country_list"))