import jwt
from datetime import datetime, timedelta
from flask import make_response, request, jsonify

SECRET_KEY = 'this is secret key'


def check_access(function):
    def wrapper(*args, **kwargs):
        access = check_authorization(request)
        if access['valid']:
            return function(*args, **kwargs)
        else:
            response = {'message': access['message']}
            return make_response(jsonify(response)), 401

    return wrapper


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
