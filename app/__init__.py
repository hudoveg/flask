from flask import Flask, request, abort, jsonify
from datetime import datetime, timedelta
import db
import jwt

SECRET_KEY = 'this is secret key'


def create_app():
    app = Flask(__name__)

    @app.route('/auth/register', methods=['POST'])
    def auth_register():
        user = request.get_json()
        conn = db.connect_database()
        if db.add_user(conn, user):
            return 'user register success'
        else:
            return 'user register fail'

    @app.route('/auth/login', methods=['POST'])
    def auth_login():
        data = request.get_json()
        conn = db.connect_database()
        user = db.get_user_by_username(conn, data['username'])
        if data['password'] == user['password']:
            access_token = generate_token(user['id'])
            if access_token:
                response = {
                    'message': 'You logged in successfully.',
                    'access_token': access_token.decode()
                }
                return jsonify(response), 200
        else:
            response = {
                'message': 'Invalid username or password, Please try again.'
            }
            return jsonify(response), 401

    @app.route('/notes', methods=['GET'])
    def note_list():
        access = check_authorization(request)
        if access['valid']:
            conn = db.connect_database()
            notes = db.get_all(conn)
            return jsonify(notes), 200
        else:
            response = {'message': access['message']}
            return jsonify(response), 401

    @app.route('/notes/add', methods=['POST'])
    def note_add():
        access = check_authorization(request)
        if access['valid']:
            note = request.get_json()
            conn = db.connect_database()
            if db.add_note(conn, note):
                response = {'message': 'notes add success'}
                return jsonify(response), 200
            else:
                response = {'message': 'notes add fail'}
                return jsonify(response), 500
        else:
            response = {'message': access['message']}
            return jsonify(response), 401

    @app.route('/notes/<int:nid>', methods=['GET', 'PUT', 'DELETE'])
    def notes_manipulation(nid):
        access = check_authorization(request)
        if access['valid']:
            conn = db.connect_database()
            if request.method == 'GET':
                note = db.get_note(conn, nid)
                if note:
                    return jsonify(note)
            elif request.method == 'PUT':
                note = request.get_json()
                note_update = db.update_note(conn, nid, note)
                return jsonify(note_update)
            else:
                if db.del_note(conn, nid):
                    return 'delete success'

            response = {'message': 'resource not found'}
            return jsonify(response), 404
        else:
            response = {'message': access['message']}
            return jsonify(response), 401

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
