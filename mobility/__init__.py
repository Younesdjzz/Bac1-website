import os
from flask import Flask, render_template
from . import stats

def create_app(test_config=None):
    """
    Créer et configure un application Flask 
    
    post:
        Retourne une instance configurée de l'application Flask.
        Les blueprints 'airport' et 'stats' sont enregistrés.
        Les routes principales ('/', '/equipe') sont définies.
        La configuration est chargée selon le mode (test ou production).
        Le dossier instance est créé s'il n'existe pas.
        La fonction db.init_app(app) a été appelée pour initialiser l'accès à la base de données.
    """
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    
    if test_config:
        app.config.from_mapping(test_config)
    else:
        app.config.from_mapping(
            SECRET_KEY="dev",
            DATABASE=os.path.join(app.instance_path, "../instance/db.sqlite"),
        )

    from . import db
    db.init_app(app)
    from . import airport
    from . import emission
    app.register_blueprint(airport.bp)
    app.register_blueprint(stats.bp)
    app.register_blueprint(emission.bp)
    
    


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

    

    # No need to call db.init_db() because we're using an existing database

    # a simple page that says hello
    @app.route('/')
    def index():
        """
        Défini les variables pour la page d'accueuil 
        """
        bienvenu = "Bienvenue sur le site web de Celestia airlines"
        membres = "Younes, Yassine, Zakaria, Adjovi, et Bouchra"

        return render_template('home.html', bienvenu=bienvenu, membres=membres)

    @app.route('/equipe')
    def equipe():
        """
        Defini les variables pour les pages de présentations de l'équipe
        """
        team = ["Younes", "Yassine", "Adjovi", "Bouchra"]
        image = ["younes.jpg", "yassine.png", "adjovi.jpg","bouchra.jpg"]
        roles = ["Front-end web designer", "Python test Specialist", "Database Management","Database Management"]
        fonds = ["#313131", "#E0403A", "#fad989","#ff66b2", "#999999"]
        couleurs = ["#ede6f3", "#F0F0F0 ", "#703A1F", "#002b17", "#333333"]
        passions = [["Jeux vidéos", "Anime (Vinland Saga)"], ["Travailler", "Anime (One piece)"], ["K-POP", "Anime", "K-drama"], ["Lecture", "Voyage"]]
        discord = ["younesdjzz", "yassne", "cadance2511", "bmoumen."]
        logos_discord = ["discord_logo_younes.png", "discord_logo_yassine.png", "discord_logo_adjovi.png", "discord_logo_bouchra.png"]

        info_equipe = zip(team, image, roles, fonds, couleurs, passions, discord, logos_discord)

        return render_template('equipe.html', info_equipe=info_equipe)
    
    return app
