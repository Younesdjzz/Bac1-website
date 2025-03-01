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
        discord = ["younesdjzz", "yassne", "zakariia_h"]
        team = ["Younes", "Yassine", "Zakaria"]
        route_team = ["/equipe/younes", "/equipe/yassine", "/equipe/zakaria"]
        image = ["younes.jpg", "yassine.png", "zakaria.jpg"]
        info_equipe = zip(team, discord, route_team, image)
        return render_template('equipe.html', info_equipe=info_equipe)
    
    @app.route('/equipe/younes')
    def younes():
        return render_template('younes.html', prenom="Younes", age="18")
    
    @app.route('/equipe/zakaria')
    def zakaria():
        return render_template('zakaria.html', prenom="Zakaria", age="18")
    @app.route('/equipe/yassine')
    def yassine():
        return render_template('yassine.html',prenom='Yassine',age='18')
    return app



