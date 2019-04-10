from flask import Blueprint
from flask.views import MethodView
from flask import make_response, request, jsonify
from .models import User, Author, Publisher, Category, Book, Review, Order, OrderItem
from .auth import generate_token, check_access
from sqlalchemy import func
from sqlalchemy import desc
from sqlalchemy.sql.functions import coalesce


def register_view(blueprint, view, endpoint, url='/', pk='record_id', pk_type='int'):
    view_func = view.as_view(endpoint)
    blueprint.add_url_rule(
        url,
        defaults={pk: None},
        view_func=view_func,
        methods=['GET']
    )
    blueprint.add_url_rule(
        url,
        view_func=view_func,
        methods=['POST']
    )
    blueprint.add_url_rule(
        '%s<%s:%s>' % (url, pk_type, pk),
        view_func=view_func,
        methods=['GET', 'PUT', 'DELETE']
    )


class RegistrationView(MethodView):
    def post(self):
        post_data = request.get_json()
        user = User.query.filter_by(username=post_data['username']).first()

        if not user:
            try:
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


auth_blueprint = Blueprint('auth', __name__)
registration_view = RegistrationView.as_view('registration_view')
login_view = LoginView.as_view('login_view')
auth_blueprint.add_url_rule(
    '/register',
    view_func=registration_view,
    methods=['POST'])
auth_blueprint.add_url_rule(
    '/login',
    view_func=login_view,
    methods=['POST']
)


class UserListView(MethodView):
    @check_access
    def get(self, record_id):
        if record_id is None:
            rows = User.query.all()
            response = []
            for row in rows:
                response.append({'id': row.id, 'username': row.username})
            return make_response(jsonify(response)), 200
        else:
            record = User.query.filter_by(id=record_id).first()
            response = {'id': record.id, 'username': record.username}
            if record:
                return make_response(jsonify(response)), 200
            else:
                response = {'message': 'resource not found'}
                return make_response(jsonify(response)), 404

    @check_access
    def post(self):
        try:
            post_data = request.get_json()
            record = User(username=post_data['username'], password=post_data['password'])
            record.save()
            response = {
                'id': record.id,
                'username': record.username
            }
            return make_response(jsonify(response)), 201
        except Exception as e:
            response = {'message': str(e)}
            return make_response(jsonify(response)), 500

    @check_access
    def put(self, record_id):
        try:
            data_put = request.get_json()
            record = User.query.filter_by(id=record_id).first()
            if record:
                username = data_put.get('username', None)
                if username:
                    record.username = username
                password = data_put.get('password', None)
                if password:
                    record.password = password
                record.save()
                response = {
                    'id': record.id,
                    'name': record.name
                }
                return make_response(jsonify(response)), 200
            else:
                response = {'message': 'user not found'}
                return make_response(jsonify(response)), 404
        except Exception as e:
            response = {'message': str(e)}
            return make_response(jsonify(response)), 500

    @check_access
    def delete(self, record_id):
        try:
            record = User.query.filter_by(id=record_id).first()
            if record:
                record.delete()
                response = {'message': 'user {} deleted'.format(record.id)}
                return make_response(jsonify(response)), 200
            else:
                response = {'message': 'resource not found'}
                return make_response(jsonify(response)), 404
        except Exception as e:
            response = {'message': str(e)}
            return make_response(jsonify(response)), 500


user_blueprint = Blueprint('users', __name__)
register_view(user_blueprint, UserListView, 'user_view')


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
register_view(author_blueprint, AuthorView, 'author_view')


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
register_view(publisher_blueprint, PublisherView, 'publisher_view')


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
register_view(category_blueprint, CategoryView, 'category_view')


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
register_view(book_blueprint, BookView, 'book_view')


@book_blueprint.route('/best-seller')
@check_access
def book_best_seller():
    rows = Book.query.\
        outerjoin(OrderItem).\
        group_by(Book.id).\
        order_by(desc(coalesce(func.sum(OrderItem.quantity), 0))).\
        all()
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


class ReviewView(MethodView):
    @check_access
    def get(self, record_id):
        if record_id is None:
            rows = Review.query.all()
            response = []
            for record in rows:
                response.append({
                    'id': record.id,
                    'username': record.user.username,
                    'book': record.book.title,
                    'rate': record.rate,
                    'title': record.title,
                    'comment': record.comment
                })
            return make_response(jsonify(response)), 200
        else:
            record = Review.query.filter_by(id=record_id).first()
            response = {
                'id': record.id,
                'username': record.user.username,
                'book': record.book.title,
                'rate': record.rate,
                'title': record.title,
                'comment': record.comment
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
            user = User.query.filter_by(username=post_data['user']).first()
            book = Book.query.filter_by(title=post_data['book']).first()
            if not user:
                response = {'message': '"user" property is require'}
                return make_response(jsonify(response)), 400
            if not book:
                response = {'message': '"book" property is require'}
                return make_response(jsonify(response)), 400

            record = Review(title=post_data['title'], user=user, book=book,
                            rate=post_data['rate'], comment=post_data['comment'])
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
                    'username': record.user.username,
                    'book': record.book.title,
                    'rate': record.rate,
                    'title': record.title,
                    'comment': record.comment
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
register_view(review_blueprint, ReviewView, 'review_view')


class OrderView(MethodView):
    @check_access
    def get(self, record_id):
        if record_id is None:
            rows = Order.query.all()
            response = []
            for row in rows:
                order = {
                    'id': row.id,
                    'user': row.user.username,
                    'total_price': row.total_price,
                    'items': [],
                    'create_at': row.created_at,
                    'update_at': row.updated_at
                }
                for item in row.items:
                    order['items'].append({
                        'id': item.id,
                        'book': item.book.title,
                        'book_id': item.book.id,
                        'quantity': item.quantity,
                        'total_price': item.total_price
                    })
                response.append(order)
            return make_response(jsonify(response)), 200
        else:
            row = Order.query.filter_by(id=record_id).first()
            if row:
                response = {
                    'id': row.id,
                    'user': row.user.username,
                    'total_price': row.total_price,
                    'items': [],
                    'create_at': row.created_at,
                    'update_at': row.updated_at
                }
                for item in row.items:
                    response['items'].append({
                        'id': item.id,
                        'book': item.book.title,
                        'book_id': item.book.id,
                        'quantity': item.quantity,
                        'total_price': item.total_price
                    })
                return make_response(jsonify(response)), 200
            else:
                response = {'message': 'resource not found'}
                return make_response(jsonify(response)), 404

    @check_access
    def post(self):
        try:
            post_data = request.get_json()
            user = User.query.filter_by(username=post_data['user']).first()
            if not user:
                return make_response(jsonify({'message': 'user is require'})), 400
            items = []
            order_total_price = 0
            for item in post_data['items']:
                book = Book.query.filter_by(title=item['book']).first()
                if not book:
                    return make_response(jsonify({'message': 'book is require'})), 400
                quantity = item['quantity']
                item_total_price = book.price * quantity
                order_total_price += item_total_price
                order_item = OrderItem(book=book, quantity=quantity, total_price=item_total_price)
                items.append(order_item)
            record = Order(user=user, items=items, total_price=order_total_price)
            record.save()
            response = {
                'id': record.id,
                'user': record.user.username,
                'total_price': record.total_price,
                'items': [],
                'create_at': record.created_at,
                'update_at': record.updated_at
            }
            for item in record.items:
                response['items'].append({
                    'id': item.id,
                    'book': item.book.title,
                    'quantity': item.quantity,
                    'total_price': item.total_price
                })
            return make_response(jsonify(response)), 201
        except Exception as e:
            response = {'message': str(e)}
            return make_response(jsonify(response)), 500

    @check_access
    def put(self, record_id):
        response = {'message': 'not implemented'}
        return make_response(jsonify(response)), 501

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
register_view(order_blueprint, OrderView, 'order_view')


class OrderItemView(MethodView):
    @check_access
    def get(self, record_id):
        if record_id is None:
            rows = OrderItem.query.all()
            response = []
            for row in rows:
                response.append({'id': row.id, 'book': row.book.title, 'quantity': row.quantity, 'total_price': row.total_price, 'order': row.order.id})
            return make_response(jsonify(response)), 200
        else:
            row = OrderItem.query.filter_by(id=record_id).first()
            response = {'id': row.id, 'book': row.book.title, 'quantity': row.quantity, 'total_price': row.total_price, 'order': row.order.id}
            if row:
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
        response = {'message': 'not implemented'}
        return make_response(jsonify(response)), 501

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
    '/<int:record_id>',
    view_func=order_item_view,
    methods=['GET']
)
