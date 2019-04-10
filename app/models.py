from app import db


class Base(db.Model):
    __abstract__ = True

    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class User(Base):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(256), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    orders = db.relationship('Order', backref='user')
    reviews = db.relationship('Review', backref='user')

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def password_is_valid(self, password):
        return self.password == password

    def __repr__(self):
        return '<%r %r>' % (__class__, self.username)


class Author(Base):
    __tablename__ = 'authors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False, unique=True)
    books = db.relationship('Book', backref='author')

    def __repr__(self):
        return '<%r %r>' % (__class__, self.name)


class Book(Base):
    """
    ONE author has MANY book
    ONE publisher has MANY book
    ONE category has MANY book
    ONE book has MANY review
    """
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'))
    publisher_id = db.Column(db.Integer, db.ForeignKey('publishers.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    title = db.Column(db.String(256))
    price = db.Column(db.Integer)
    reviews = db.relationship('Review', backref='book')

    def __repr__(self):
        return '<%r %r>' % (__class__, self.title)


class Publisher(Base):
    __tablename__ = 'publishers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False, unique=True)
    books = db.relationship('Book', backref='publisher')

    def __repr__(self):
        return '<%r %r>' % (__class__, self.name)


class Category(Base):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False, unique=True)
    books = db.relationship('Book', backref='category')

    def __repr__(self):
        return '<%r %r>' % (__class__, self.name)


class Review(Base):
    """
    ONE book has MANY review
    ONE user has MANY review
    """
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    rate = db.Column(db.Integer)
    title = db.Column(db.String(256))
    comment = db.Column(db.Text)

    def __repr__(self):
        return '<%r %r>' % (__class__, self.title)


class Order(Base):
    """
    ONE order has MANY item
    ONE user has MANY order
    """
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    items = db.relationship('OrderItem', backref='order', cascade="all, delete, delete-orphan")
    total_price = db.Column(db.Integer)

    def __repr__(self):
        return '<%r %d>' % (__class__, self.id)


class OrderItem(Base):
    __tablename__ = 'order_items'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    quantity = db.Column(db.Integer)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'))
    book = db.relationship('Book')
    total_price = db.Column(db.Integer)

    def __repr__(self):
        return '<%r %d>' % (__class__, self.id)
