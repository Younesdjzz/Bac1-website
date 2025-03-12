from flask import (
    Blueprint, render_template, request, redirect, url_for
)
from mobility.models.stats import get_country_list, search_by_iso, Country


# route code
@bp.route('/statistique')
def country_list():
    countries = get_country_list()
    return render_template("statistique.html", countries=countries)

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