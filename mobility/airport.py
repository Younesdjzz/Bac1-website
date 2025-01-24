from flask import (
      Blueprint, render_template
)

from mobility.models.airport import get_airports

bp = Blueprint('airport', __name__)

# Define the routes code
@bp.route('/')
def airport_list():
    airports = get_airports()
    return render_template("airports.html", airports=airports)
