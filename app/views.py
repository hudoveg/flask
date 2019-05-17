from flask import Blueprint
from flask.views import MethodView
from flask import make_response, request, jsonify, current_app
from .models import User, Author, Publisher, Category, Book, Review, Order, OrderItem
from .auth import generate_token, check_access
from sqlalchemy import func, desc, cast, FLOAT
from sqlalchemy.sql.functions import coalesce
from sqlalchemy.dialects import postgresql


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
        """

        :return:
        """
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


@author_blueprint.route('/best-selling')
def author_best_selling():
    """
    SELECT authors.*, COALESCE(SUM(order_items.quantity), 0) as quantity_sold
    FROM authors
    JOIN books ON authors.id = books.author_id
    JOIN order_items ON order_items.book_id = books.id
    GROUP BY authors.id
    ORDER BY quantity_sold DESC
    """
    q = Author.query. \
        add_column(func.sum(OrderItem.quantity).label('quantity_sold')). \
        join(Author.books). \
        join(OrderItem, Book.id == OrderItem.book_id). \
        group_by(Author.id). \
        order_by(desc('quantity_sold'))
    # return str(q.statement.compile(dialect=postgresql.dialect()))
    rows = q.all()
    response = []
    for record in rows:
        response.append({
            'id': record.Author.id,
            'name': record.Author.name,
            'quantity_sold': record.quantity_sold
        })
    return make_response(jsonify(response)), 200


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


@book_blueprint.route('/best-selling')
@check_access
def book_best_selling():
    """
    SELECT books.*, COALESCE(SUM(order_items.quantity), 0) as quantity_sold
    FROM books LEFT OUTER JOIN order_items ON books.id = order_items.book_id
    GROUP BY books.id
    ORDER BY quantity_sold DESC;
    """
    rows = Book.query.\
        add_column(coalesce(func.sum(OrderItem.quantity), 0).label('quantity_sold')).\
        outerjoin(OrderItem).\
        group_by(Book.id).\
        order_by(desc('quantity_sold')).\
        all()
    response = []
    for record in rows:
        response.append({
            'id': record.Book.id,
            'title': record.Book.title,
            'author': record.Book.author.name,
            'publisher': record.Book.publisher.name,
            'category': record.Book.category.name,
            'price': record.Book.price,
            'quantity_sold': record.quantity_sold
        })
    return make_response(jsonify(response)), 200


@book_blueprint.route('/best-rating')
def book_best_rating():
    """
    SELECT books.*, COALESCE(SUM(reviews.rate) / COUNT(reviews), 0) as rating
    FROM books LEFT OUTER JOIN reviews ON books.id = reviews.book_id
    GROUP BY books.id
    ORDER BY rating DESC;
    """
    rating_col = coalesce(cast(func.sum(Review.rate), FLOAT)/cast(func.count(Review.id), FLOAT), 0).\
        label('rating')
    rows = Book.query.\
        add_column(rating_col). \
        outerjoin(Review).\
        group_by(Book.id).\
        order_by(desc('rating')).\
        all()
    response = []
    for record in rows:
        response.append({
            'id': record.Book.id,
            'title': record.Book.title,
            'author': record.Book.author.name,
            'publisher': record.Book.publisher.name,
            'category': record.Book.category.name,
            'price': record.Book.price,
            'rating': record.rating
        })
    return make_response(jsonify(response)), 200


@book_blueprint.route('/literature/best-selling')
def literature_books_best_selling():
    """
    SELECT books.*, literature_books_best_selling.quantity_sold
    FROM books
    JOIN (
        SELECT literature_books.id, COALESCE(SUM(order_items.quantity), 0) as quantity_sold
        FROM (SELECT * FROM books WHERE books.category_id = 2) AS literature_books
        LEFT OUTER JOIN order_items ON literature_books.id = order_items.book_id
        GROUP BY literature_books.id
        ORDER BY quantity_sold DESC
    ) AS literature_books_best_selling ON books.id = literature_books_best_selling.id;
    """
    literature_books = Book.query.\
        with_entities(Book.id).\
        filter_by(category_id=2).\
        from_self().\
        add_column(coalesce(func.sum(OrderItem.quantity), 0).label('quantity_sold')).\
        outerjoin(OrderItem).\
        group_by(Book.id).\
        order_by(desc('quantity_sold')).\
        subquery().alias()

    rows = Book.query.join(literature_books, literature_books.c.books_id == Book.id).\
        add_column(literature_books.c.quantity_sold).\
        all()
    response = []
    for record in rows:
        response.append({
            'id': record.Book.id,
            'title': record.Book.title,
            'author': record.Book.author.name,
            'publisher': record.Book.publisher.name,
            'category': record.Book.category.name,
            'price': record.Book.price,
            'quantity_sold': record.quantity_sold
        })
    return make_response(jsonify(response)), 200


@book_blueprint.route('/search')
def book_search():
    """
    SELECT books.*
    FROM books
    JOIN authors ON books.author_id = authors.id
    WHERE authors.name LIKE '%' + @name '%' AND books.title LIKE '%' + @title + '%'
    """

    author_name = request.args.get('author')
    book_title = request.args.get('title')
    category_name = request.args.get('category')

    q = Book.query

    if author_name:
        q = q.join(Author).filter(Author.name.ilike('{}%'.format(author_name)))
    if book_title:
        q = q.filter(Book.title.ilike('%{}%'.format(book_title)))
    if category_name:
        q = q.join(Category).filter(Category.name.ilike('%{}'.format(category_name)))

    q.order_by(desc(Book.updated_at))
    # return str(q.statement.compile(dialect=postgresql.dialect()))

    current_app.logger.info(str(q.statement.compile(dialect=postgresql.dialect(),
                                                    compile_kwargs={"literal_binds": True})))
    response = []
    for record in q:
        response.append({
            'id': record.id,
            'title': record.title,
            'author': record.author.name,
            'publisher': record.publisher.name,
            'category': record.category.name,
            'price': record.price,
        })
        current_app.logger.info(repr(record))
    try:
        raise Exception('it must be an exception')
    except Exception as e:
        current_app.logger.exception(str(e))
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
