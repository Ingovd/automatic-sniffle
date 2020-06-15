import os

from flask import Flask

from google.cloud import datastore

APP_CREATED_FLASK_1PATH = "Created Flask application in folder: {}"

def create_app(config={}):
    if path := config.get('INSTANCE_PATH'):
        app = Flask(__name__, instance_path=path)
    else:
        app = Flask(__name__, instance_relative_config=True)
    app.logger.info(APP_CREATED_FLASK_1PATH.format(app.instance_path))
    app.config.from_pyfile(os.path.join(app.instance_path, 'config.py'))
    app.config.update(config)

    if config["PROJECT"] is None:
        exit("No project ID specified in kwargs or config.py")

    with app.app_context():
        app.db = datastore.Client(project=app.config["PROJECT"])
        from jigs.routes import jig_bp
        app.register_blueprint(jig_bp)
    return app
