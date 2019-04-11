from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from instance.config import app_config

# initialize db
db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(app_config[config_name])
    db.init_app(app)

    from .views import auth_blueprint, author_blueprint, user_blueprint
    from .views import publisher_blueprint, category_blueprint, book_blueprint
    from .views import review_blueprint, order_blueprint, order_item_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(user_blueprint, url_prefix='/users')
    app.register_blueprint(author_blueprint, url_prefix='/authors')
    app.register_blueprint(publisher_blueprint, url_prefix='/publishers')
    app.register_blueprint(category_blueprint, url_prefix='/categories')
    app.register_blueprint(book_blueprint, url_prefix='/books')
    app.register_blueprint(review_blueprint, url_prefix='/reviews')
    app.register_blueprint(order_blueprint, url_prefix='/orders')
    app.register_blueprint(order_item_blueprint, url_prefix='/order-items')

    return app
