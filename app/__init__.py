from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import jwt


# initialize db
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config['DEBUG'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:postgres@127.0.0.1:5432/flask_api'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    from .views import auth_blueprint, note_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(note_blueprint, url_prefix='/notes')

    return app
