from flask import Blueprint
from flask.views import MethodView
from flask import make_response, request, jsonify, abort
from .models import User, Note, Author, Publisher, Category, Book, Review, Order, OrderItem
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


note_blueprint = Blueprint('note', __name__)

note_view = NoteView.as_view('note_view')

note_blueprint.add_url_rule(
    '/',
    defaults={'note_id': None},
    view_func=note_view,
    methods=['GET']
)
note_blueprint.add_url_rule(
    '/',
    view_func=note_view,
    methods=['POST']
)
note_blueprint.add_url_rule(
    '/<int:note_id>',
    view_func=note_view,
    methods=['GET', 'PUT', 'DELETE']
)


class AuthorView(MethodView):
    @check_access
    def get(self, record_id):
        if record_id is None:
            rows = Author.query.all()
            response = []
            for row in rows:
                response.append({'id': row.id, 'name': row.name})
            return make_response(jsonify(response)), 200
        else:
            record = Author.query.filter_by(id=record_id).first()
            response = {'id': record.id, 'name': record.name}
            if record:
                return make_response(jsonify(response)), 200
            else:
                response = {'message': 'resource not found'}
                return make_response(jsonify(response)), 404

    @check_access
    def post(self):
        try:
            post_data = request.get_json()
            record = Author(name=post_data['name'])
            record.save()
            response = {
                'id': record.id,
                'name': record.name
            }
            return make_response(jsonify(response)), 201
        except Exception as e:
            response = {'message': str(e)}
            return make_response(jsonify(response)), 500

    @check_access
    def put(self, record_id):
        try:
            data_put = request.get_json()
            record = Author.query.filter_by(id=record_id).first()
            if record:
                name = data_put.get('name', None)
                if name:
                    record.name = name
                record.save()
                response = {
                    'id': record.id,
                    'name': record.name
                }
                return make_response(jsonify(response)), 200
            else:
                response = {'message': 'resource not found'}
                return make_response(jsonify(response)), 404
        except Exception as e:
            response = {'message': str(e)}
            return make_response(jsonify(response)), 500

    @check_access
    def delete(self, record_id):
        try:
            record = Author.query.filter_by(id=record_id).first()
            if record:
                record.delete()
                response = {'message': 'author {} deleted'.format(record.id)}
                return make_response(jsonify(response)), 200
            else:
                response = {'message': 'resource not found'}
                return make_response(jsonify(response)), 404
        except Exception as e:
            response = {'message': str(e)}
            return make_response(jsonify(response)), 500


author_blueprint = Blueprint('author', __name__)

author_view = AuthorView.as_view('author_view')

author_blueprint.add_url_rule(
    '/',
    defaults={'record_id': None},
    view_func=author_view,
    methods=['GET']
)
author_blueprint.add_url_rule(
    '/',
    view_func=author_view,
    methods=['POST']
)
author_blueprint.add_url_rule(
    '/<int:record_id>',
    view_func=author_view,
    methods=['GET', 'PUT', 'DELETE']
)


class PublisherView(MethodView):
    @check_access
    def get(self, record_id):
        if record_id is None:
            rows = Publisher.query.all()
            response = []
            for row in rows:
                response.append({'id': row.id, 'name': row.name})
            return make_response(jsonify(response)), 200
        else:
            record = Publisher.query.filter_by(id=record_id).first()
            response = {'id': record.id, 'name': record.name}
            if record:
                return make_response(jsonify(response)), 200
            else:
                response = {'message': 'resource not found'}
                return make_response(jsonify(response)), 404

    @check_access
    def post(self):
        try:
            post_data = request.get_json()
            record = Publisher(name=post_data['name'])
            record.save()
            response = {
                'id': record.id,
                'name': record.name
            }
            return make_response(jsonify(response)), 201
        except Exception as e:
            response = {'message': str(e)}
            return make_response(jsonify(response)), 500

    @check_access
    def put(self, record_id):
        try:
            data_put = request.get_json()
            record = Publisher.query.filter_by(id=record_id).first()
            if record:
                name = data_put.get('name', None)
                if name:
                    record.name = name
                record.save()
                response = {
                    'id': record.id,
                    'name': record.name
                }
                return make_response(jsonify(response)), 200
            else:
                response = {'message': 'resource not found'}
                return make_response(jsonify(response)), 404
        except Exception as e:
            response = {'message': str(e)}
            return make_response(jsonify(response)), 500

    @check_access
    def delete(self, record_id):
        try:
            record = Publisher.query.filter_by(id=record_id).first()
            if record:
                record.delete()
                response = {'message': 'publisher {} deleted'.format(record.id)}
                return make_response(jsonify(response)), 200
            else:
                response = {'message': 'resource not found'}
                return make_response(jsonify(response)), 404
        except Exception as e:
            response = {'message': str(e)}
            return make_response(jsonify(response)), 500


publisher_blueprint = Blueprint('publisher', __name__)

publisher_view = PublisherView.as_view('publisher_view')

publisher_blueprint.add_url_rule(
    '/',
    defaults={'record_id': None},
    view_func=publisher_view,
    methods=['GET']
)
publisher_blueprint.add_url_rule(
    '/',
    view_func=publisher_view,
    methods=['POST']
)
publisher_blueprint.add_url_rule(
    '/<int:record_id>',
    view_func=publisher_view,
    methods=['GET', 'PUT', 'DELETE']
)


class CategoryView(MethodView):
    @check_access
    def get(self, record_id):
        if record_id is None:
            rows = Category.query.all()
            response = []
            for row in rows:
                response.append({'id': row.id, 'name': row.name})
            return make_response(jsonify(response)), 200
        else:
            record = Category.query.filter_by(id=record_id).first()
            response = {'id': record.id, 'name': record.name}
            if record:
                return make_response(jsonify(response)), 200
            else:
                response = {'message': 'resource not found'}
                return make_response(jsonify(response)), 404

    @check_access
    def post(self):
        try:
            post_data = request.get_json()
            record = Category(name=post_data['name'])
            record.save()
            response = {
                'id': record.id,
                'name': record.name
            }
            return make_response(jsonify(response)), 201
        except Exception as e:
            response = {'message': str(e)}
            return make_response(jsonify(response)), 500

    @check_access
    def put(self, record_id):
        try:
            data_put = request.get_json()
            record = Category.query.filter_by(id=record_id).first()
            if record:
                name = data_put.get('name', None)
                if name:
                    record.name = name
                record.save()
                response = {
                    'id': record.id,
                    'name': record.name
                }
                return make_response(jsonify(response)), 200
            else:
                response = {'message': 'resource not found'}
                return make_response(jsonify(response)), 404
        except Exception as e:
            response = {'message': str(e)}
            return make_response(jsonify(response)), 500

    @check_access
    def delete(self, record_id):
        try:
            record = Category.query.filter_by(id=record_id).first()
            if record:
                record.delete()
                response = {'message': 'category {} deleted'.format(record.id)}
                return make_response(jsonify(response)), 200
            else:
                response = {'message': 'resource not found'}
                return make_response(jsonify(response)), 404
        except Exception as e:
            response = {'message': str(e)}
            return make_response(jsonify(response)), 500


category_blueprint = Blueprint('category', __name__)

category_view = CategoryView.as_view('category_view')

category_blueprint.add_url_rule(
    '/',
    defaults={'record_id': None},
    view_func=category_view,
    methods=['GET']
)
category_blueprint.add_url_rule(
    '/',
    view_func=category_view,
    methods=['POST']
)
category_blueprint.add_url_rule(
    '/<int:record_id>',
    view_func=category_view,
    methods=['GET', 'PUT', 'DELETE']
)


class BookView(MethodView):
    @check_access
    def get(self, record_id):
        if record_id is None:
            rows = Book.query.all()
            response = []
            for record in rows:
                response.append({
                    'id': record.id,
                    'title': record.title,
                    'author': record.author.name,
                    'publisher': record.publisher.name,
                    'category': record.category.name,
                    'price': record.price
                })
            return make_response(jsonify(response)), 200
        else:
            record = Book.query.filter_by(id=record_id).first()
            response = {
                'id': record.id,
                'title': record.title,
                'author': record.author.name,
                'publisher': record.publisher.name,
                'category': record.category.name,
                'price': record.price
            }
            if record:
                return make_response(jsonify(response)), 200
            else:
                response = {'message': 'resource not found'}
                return make_response(jsonify(response)), 404

    @check_access
    def post(self):
        try:
            post_data = request.get_json()
            author = Author.query.filter_by(name=post_data['author']).first()
            if not author:
                author = Author(name=post_data['author'])
                author.save()
            publisher = Publisher.query.filter_by(name=post_data['publisher']).first()
            if not publisher:
                publisher = Publisher(name=post_data['publisher'])
                publisher.save()
            category = Category.query.filter_by(name=post_data['category']).first()
            if not category:
                category = Category(name=post_data['category'])
                category.save()

            record = Book(title=post_data['title'], author=author, publisher=publisher,
                          category=category, price=post_data['price'])
            record.save()
            response = {
                'id': record.id,
                'title': record.title,
                'author': record.author.name,
                'publisher': record.publisher.name,
                'category': record.category.name,
                'price': record.price
            }
            return make_response(jsonify(response)), 201
        except Exception as e:
            response = {'message': str(e)}
            return make_response(jsonify(response)), 500

    @check_access
    def put(self, record_id):
        try:
            data_put = request.get_json()
            record = Book.query.filter_by(id=record_id).first()
            if record:
                title = data_put.get('title', None)
                if title:
                    record.title = title
                price = data_put.get('price', None)
                if price:
                    record.price = price
                record.save()
                response = {
                    'id': record.id,
                    'title': record.title,
                    'author': record.author.name,
                    'publisher': record.publisher.name,
                    'category': record.category.name,
                    'price': record.price
                }
                return make_response(jsonify(response)), 200
            else:
                response = {'message': 'resource not found'}
                return make_response(jsonify(response)), 404
        except Exception as e:
            response = {'message': str(e)}
            return make_response(jsonify(response)), 500

    @check_access
    def delete(self, record_id):
        try:
            record = Book.query.filter_by(id=record_id).first()
            if record:
                record.delete()
                response = {'message': 'book {} deleted'.format(record.id)}
                return make_response(jsonify(response)), 200
            else:
                response = {'message': 'resource not found'}
                return make_response(jsonify(response)), 404
        except Exception as e:
            response = {'message': str(e)}
            return make_response(jsonify(response)), 500


book_blueprint = Blueprint('book', __name__)

book_view = BookView.as_view('book_view')

book_blueprint.add_url_rule(
    '/',
    defaults={'record_id': None},
    view_func=book_view,
    methods=['GET']
)
book_blueprint.add_url_rule(
    '/',
    view_func=book_view,
    methods=['POST']
)
book_blueprint.add_url_rule(
    '/<int:record_id>',
    view_func=book_view,
    methods=['GET', 'PUT', 'DELETE']
)


class ReviewView(MethodView):
    @check_access
    def get(self, record_id):
        if record_id is None:
            rows = Review.query.all()
            response = []
            for row in rows:
                response.append({'id': row.id, 'name': row.name})
            return make_response(jsonify(response)), 200
        else:
            record = Review.query.filter_by(id=record_id).first()
            response = {'id': record.id, 'name': record.name}
            if record:
                return make_response(jsonify(response)), 200
            else:
                response = {'message': 'resource not found'}
                return make_response(jsonify(response)), 404

    @check_access
    def post(self):
        try:
            post_data = request.get_json()
            record = Review(post_data['name'])
            record.save()
            response = {
                'id': record.id,
                'username': record.user.username,
                'book': record.book.title,
                'rate': record.rate,
                'title': record.title,
                'comment': record.comment
            }
            return make_response(jsonify(response)), 201
        except Exception as e:
            response = {'message': str(e)}
            return make_response(jsonify(response)), 500

    @check_access
    def put(self, record_id):
        try:
            data_put = request.get_json()
            record = Review.query.filter_by(id=record_id).first()
            if record:
                name = data_put.get('name', None)
                if name:
                    record.name = name
                record.save()
                response = {
                    'id': record.id,
                    'name': record.name
                }
                return make_response(jsonify(response)), 200
            else:
                response = {'message': 'resource not found'}
                return make_response(jsonify(response)), 404
        except Exception as e:
            response = {'message': str(e)}
            return make_response(jsonify(response)), 500

    @check_access
    def delete(self, record_id):
        try:
            record = Review.query.filter_by(id=record_id).first()
            if record:
                record.delete()
                response = {'message': 'review {} deleted'.format(record.id)}
                return make_response(jsonify(response)), 200
            else:
                response = {'message': 'resource not found'}
                return make_response(jsonify(response)), 404
        except Exception as e:
            response = {'message': str(e)}
            return make_response(jsonify(response)), 500


review_blueprint = Blueprint('review', __name__)

review_view = ReviewView.as_view('review_view')

review_blueprint.add_url_rule(
    '/',
    defaults={'record_id': None},
    view_func=review_view,
    methods=['GET']
)
review_blueprint.add_url_rule(
    '/',
    view_func=review_view,
    methods=['POST']
)
review_blueprint.add_url_rule(
    '/<int:record_id>',
    view_func=review_view,
    methods=['GET', 'PUT', 'DELETE']
)


class OrderView(MethodView):
    @check_access
    def get(self, record_id):
        if record_id is None:
            rows = Order.query.all()
            response = []
            for row in rows:
                response.append({'id': row.id, 'name': row.name})
            return make_response(jsonify(response)), 200
        else:
            record = Order.query.filter_by(id=record_id).first()
            response = {'id': record.id, 'name': record.name}
            if record:
                return make_response(jsonify(response)), 200
            else:
                response = {'message': 'resource not found'}
                return make_response(jsonify(response)), 404

    @check_access
    def post(self):
        try:
            post_data = request.get_json()
            record = Order(post_data['name'])
            record.save()
            response = {
                'id': record.id,
                'name': record.name
            }
            return make_response(jsonify(response)), 201
        except Exception as e:
            response = {'message': str(e)}
            return make_response(jsonify(response)), 500

    @check_access
    def put(self, record_id):
        try:
            data_put = request.get_json()
            record = Order.query.filter_by(id=record_id).first()
            if record:
                name = data_put.get('name', None)
                if name:
                    record.name = name
                record.save()
                response = {
                    'id': record.id,
                    'name': record.name
                }
                return make_response(jsonify(response)), 200
            else:
                response = {'message': 'resource not found'}
                return make_response(jsonify(response)), 404
        except Exception as e:
            response = {'message': str(e)}
            return make_response(jsonify(response)), 500

    @check_access
    def delete(self, record_id):
        try:
            record = Order.query.filter_by(id=record_id).first()
            if record:
                record.delete()
                response = {'message': 'order {} deleted'.format(record.id)}
                return make_response(jsonify(response)), 200
            else:
                response = {'message': 'resource not found'}
                return make_response(jsonify(response)), 404
        except Exception as e:
            response = {'message': str(e)}
            return make_response(jsonify(response)), 500


order_blueprint = Blueprint('order', __name__)

order_view = OrderView.as_view('order_view')

order_blueprint.add_url_rule(
    '/',
    defaults={'record_id': None},
    view_func=order_view,
    methods=['GET']
)
order_blueprint.add_url_rule(
    '/',
    view_func=order_view,
    methods=['POST']
)
order_blueprint.add_url_rule(
    '/<int:record_id>',
    view_func=order_view,
    methods=['GET', 'PUT', 'DELETE']
)


class OrderItemView(MethodView):
    @check_access
    def get(self, record_id):
        if record_id is None:
            rows = OrderItem.query.all()
            response = []
            for row in rows:
                response.append({'id': row.id, 'name': row.name})
            return make_response(jsonify(response)), 200
        else:
            record = OrderItem.query.filter_by(id=record_id).first()
            response = {'id': record.id, 'name': record.name}
            if record:
                return make_response(jsonify(response)), 200
            else:
                response = {'message': 'resource not found'}
                return make_response(jsonify(response)), 404

    @check_access
    def post(self):
        try:
            post_data = request.get_json()
            record = OrderItem(post_data['name'])
            record.save()
            response = {
                'id': record.id,
                'name': record.name
            }
            return make_response(jsonify(response)), 201
        except Exception as e:
            response = {'message': str(e)}
            return make_response(jsonify(response)), 500

    @check_access
    def put(self, record_id):
        try:
            data_put = request.get_json()
            record = OrderItem.query.filter_by(id=record_id).first()
            if record:
                name = data_put.get('name', None)
                if name:
                    record.name = name
                record.save()
                response = {
                    'id': record.id,
                    'name': record.name
                }
                return make_response(jsonify(response)), 200
            else:
                response = {'message': 'resource not found'}
                return make_response(jsonify(response)), 404
        except Exception as e:
            response = {'message': str(e)}
            return make_response(jsonify(response)), 500

    @check_access
    def delete(self, record_id):
        try:
            record = OrderItem.query.filter_by(id=record_id).first()
            if record:
                record.delete()
                response = {'message': 'order item {} deleted'.format(record.id)}
                return make_response(jsonify(response)), 200
            else:
                response = {'message': 'resource not found'}
                return make_response(jsonify(response)), 404
        except Exception as e:
            response = {'message': str(e)}
            return make_response(jsonify(response)), 500


order_item_blueprint = Blueprint('order_item', __name__)

order_item_view = OrderItemView.as_view('order_item_view')

order_item_blueprint.add_url_rule(
    '/',
    defaults={'record_id': None},
    view_func=order_item_view,
    methods=['GET']
)
order_item_blueprint.add_url_rule(
    '/',
    view_func=order_item_view,
    methods=['POST']
)
order_item_blueprint.add_url_rule(
    '/<int:record_id>',
    view_func=order_item_view,
    methods=['GET', 'PUT', 'DELETE']
)
