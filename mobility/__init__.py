import os
from flask import Flask, render_template
from . import stats


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    
    if test_config:
        app.config.from_mapping(test_config)
    else:
        app.config.from_mapping(
            SECRET_KEY="dev",
            DATABASE=os.path.join(app.instance_path, "../instance/db.sqlite"),
        )

    from . import airport
    app.register_blueprint(airport.bp)
    app.register_blueprint(stats.bp)
    


    app.add_url_rule('/', endpoint='index')

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)

    # No need to call db.init_db() because we're using an existing database

    # a simple page that says hello
    @app.route('/')
    def index():
        bienvenu = "Bienvenue sur le site web de Celestia airlines"
        membres = "Younes, Yassine, Zakaria, Adjovi, et Bouchra"

        return render_template('home.html', bienvenu=bienvenu, membres=membres)

    @app.route('/equipe')
    def equipe():
        team = ["Younes", "Yassine", "Adjovi", "Bouchra", "Zakaria",]
        image = ["younes.jpg", "yassine.png", "adjovi.jpg","bouchra.jpg", "zakaria.jpg"]
        roles = ["Front-end web designer", "Is choosing a role...", "Database Management","Database Management", "Is choosing a role...",]
        fonds = ["#313131", "#E0403A", "#fad989","#ff66b2", "#999999"]
        couleurs = ["#ede6f3", "#F0F0F0 ", "#703A1F", "#002b17", "#333333"]
        passions = [["Jeux vidéos", "Anime (Vinland Saga)"], ["Travailler", "Anime (One piece)"], ["K-POP", "Anime", "K-drama"], ["Lecture", "Voyage"], ["Sport", "Voyage"]]
        discord = ["younesdjzz", "yassne", "cadance2511", "bmoumen.", "zakariia_h"]
        logos_discord = ["discord_logo_younes.png", "discord_logo_yassine.png", "discord_logo_adjovi.png", "discord_logo_bouchra.png", "discord_logo_zakaria.png"]

        info_equipe = zip(team, image, roles, fonds, couleurs, passions, discord, logos_discord)

        return render_template('equipe.html', info_equipe=info_equipe)
    
    return app
