from flask import Blueprint
from flask.views import MethodView
from flask import make_response, request, jsonify, abort
from .models import User, Note
from .auth import generate_token, check_access


auth_blueprint = Blueprint('auth', __name__)


class RegistrationView(MethodView):
    def post(self):
        user = User.query.filter_by(username=request.data['username']).first()

        if not user:
            try:
                post_data = request.data
                username = post_data['username']
                password = post_data['password']
                user = User(username, password)
                user.save()

                response = {
                    'message': 'You registered successfully. Please login.',
                }
                return make_response(jsonify(response)), 201

            except Exception as e:
                response = {
                    'message': str(e)
                }
                return make_response(jsonify(response)), 401
        else:
            response = {
                'message': 'User already exists. Please login.'
            }

            return make_response(jsonify(response)), 202


class LoginView(MethodView):
    def post(self):
        try:
            data_post = request.get_json()
            user = User.query.filter_by(username=data_post['username']).first()

            if user and user.password_is_valid(data_post['password']):
                access_token = generate_token(user.id)
                if access_token:
                    response = {
                        'message': 'You logged in successfully.',
                        'access_token': access_token.decode()
                    }
                    return make_response(jsonify(response)), 200
            else:
                response = {
                    'message': 'Invalid username or password, Please try again.'
                }
                return make_response(jsonify(response)), 401
        except Exception as e:
            response = {
                'message': str(e)
            }
            return make_response(jsonify(response)), 500


# Define the API resource
registration_view = RegistrationView.as_view('registration_view')
login_view = LoginView.as_view('login_view')

# Add the url rule for registering a user
auth_blueprint.add_url_rule(
    '/register',
    view_func=registration_view,
    methods=['POST'])
auth_blueprint.add_url_rule(
    '/login',
    view_func=login_view,
    methods=['POST']
)

note_blueprint = Blueprint('note', __name__)


class NoteView(MethodView):
    @check_access
    def get(self, note_id):
        if note_id is None:
            # return a list of notes
            notes = Note.query.all()
            response = []
            for note in notes:
                response.append({'id': note.id, 'title': note.title, 'body': note.body})
            return make_response(jsonify(response)), 200
        else:
            # expose a single note
            note = Note.query.filter_by(id=note_id).first()
            response = {'id': note.id, 'title': note.title, 'body': note.body}
            if note:
                return make_response(jsonify(response)), 200
            else:
                abort(404)

    @check_access
    def post(self):
        try:
            post_data = request.get_json()
            note = Note(post_data['title'], post_data['body'])
            note.save()
            response = {
                'id': note.id,
                'title': note.title,
                'body': note.body
            }
            return make_response(jsonify(response)), 201
        except Exception as e:
            response = {'message': str(e)}
            return make_response(jsonify(response)), 500

    @check_access
    def put(self, note_id):
        try:
            data_put = request.get_json()
            note = Note.query.filter_by(id=note_id).first()
            if note:
                title = data_put.get('title', None)
                body = data_put.get('body', None)
                if title:
                    note.title = title
                if body:
                    note.body = body
                note.save()
                response = {
                    'id': note.id,
                    'title': note.title,
                    'body': note.body
                }
                return make_response(jsonify(response)), 200
            else:
                abort(404)
        except Exception as e:
            response = {'message': str(e)}
            return make_response(jsonify(response)), 500

    @check_access
    def delete(self, note_id):
        try:
            note = Note.query.filter_by(id=note_id).first()
            if note:
                note.delete()
                response = {'message': 'note {} deleted'.format(note.id)}
                return make_response(jsonify(response)), 200
            else:
                abort(404)
        except Exception as e:
            response = {'message': str(e)}
            return make_response(jsonify(response)), 500


note_view = NoteView.as_view('note_view')

note_blueprint.add_url_rule(
    '/',
    defaults={'note_id': None},
    view_func=note_view,
    methods=['GET', 'POST']
)
note_blueprint.add_url_rule(
    '/<int:note_id>',
    view_func=note_view,
    methods=['GET', 'PUT', 'DELETE']
)
