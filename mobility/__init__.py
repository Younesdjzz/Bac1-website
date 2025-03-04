import os
from flask import Flask, render_template


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    if test_config:
        app.config.from_mapping(test_config)
    else:
        app.config.from_mapping(
            SECRET_KEY='dev',
            DATABASE=os.path.join(app.root_path, 'poudlard.sqlite'),
        )

    from . import airport
    app.register_blueprint(airport.bp)

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

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    @app.route('/equipe')
    def equipe():
        discord = ["younesdjzz", "yassne", "zakariia_h","cadance2511"]
        team = ["Younes", "Yassine", "Zakaria","Adjovi"]
        route_team = ["/equipe/younes", "/equipe/yassine", "/equipe/zakaria","/equipe/adjovi"]
        image = ["younes.jpg", "yassine.png", "zakaria.jpg","adjovi.jpg"]
        info_equipe = zip(team, discord, route_team, image)
        return render_template('equipe.html', info_equipe=info_equipe)
    
    @app.route('/equipe/younes')
    def younes():
        roles = ["Je suis actuellement le barreur du groupe",
                 "Je m'occupe de surveiller l'avancement du projet...",
                 "...et à motiver mon équipe à avancer !"]
        
        passions = ["J'aime passer mon temps libre à jouer aux jeux vidéos",
                    "J'aime bien les animes, surtout One piece et Vinland Saga",
                    "A part ça, j'aime bien aussi m'entrainer !"]
        
        return render_template('base_membre.html', prenom="Younes", age="18", roles=roles, passions=passions)
    
    @app.route('/equipe/zakaria')
    def zakaria():
        return render_template('zakaria.html', prenom="Zakaria", age="18")
    
    @app.route('/equipe/yassine')
    def yassine():
        return render_template('yassine.html',prenom='Yassine',age='18')
    
    @app.route("/equipe/adjovi")
    def adjovi():

        roles = ["Je suis en ce moment la maitresse du temps, je veille à ce que les échéances soient respectées.", 
                 "Tic-Tac..."]

        passions = ["Lorsque je n'étudie pas pour l'université, j'apprends les chorégraphies de mes chansons préférées (≧∀≦)",
                    "J'aime énormément la K-POP et l'univers qui lui est associé !",
                    "En pralant d'univers, j'apprécie également celui des animés, k-drama ou autres séries asiatiques ^^"]
        
        return render_template("base_membre.html",prenom="Adjovi",age="18",roles=roles,passions=passions)
    return app



