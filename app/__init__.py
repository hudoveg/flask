from flask import Flask
from datetime import datetime, timedelta
from flask_sqlalchemy import SQLAlchemy
import jwt

SECRET_KEY = 'this is secret key'

# initialize db
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config['DEBUG'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:postgres@127.0.0.1:5432/flask_api'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    from .views import auth_blueprint, note_blueprint
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(note_blueprint)

    return app


def generate_token(user_id):
    payload = {
        'exp': datetime.utcnow() + timedelta(minutes=5),
        'iat': datetime.utcnow(),
        'sub': user_id
    }
    # create the byte string token using the payload and the SECRET key
    jwt_string = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm='HS256'
    )
    return jwt_string


def decode_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY)
        return payload['sub']
    except jwt.ExpiredSignatureError:
        return "Expired token. Please log in to get a new token"
    except jwt.InvalidTokenError:
        return "Invalid token. Please register or login"


def check_authorization(request):
    auth_header = request.headers.get('Authorization')
    message = "Missing access token"
    if auth_header:
        access_token = auth_header.split(" ")[1]
        if access_token:
            user_id = decode_token(access_token)
            if not isinstance(user_id, str):
                return {'valid': True, 'user_id': user_id}
            else:
                message = user_id

    return {'valid': False, 'message': message}
