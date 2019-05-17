import os
import logging
from app import create_app
from logging.handlers import RotatingFileHandler
from flask import request


class RequestFormatter(logging.Formatter):
    def format(self, record):
        record.url = request.url
        record.remote_addr = request.remote_addr
        return super().format(record)


formatter = RequestFormatter(
    '[%(asctime)s] %(remote_addr)s requested %(url)s\n'
    '%(levelname)s in %(module)s: %(message)s\n'
    '======================================='
)

handler = RotatingFileHandler('test.log', maxBytes=10000, backupCount=1)
handler.setLevel(logging.INFO)
handler.setFormatter(formatter)

config_name = os.getenv('APP_SETTINGS')
app = create_app(config_name)
app.logger.addHandler(handler)

if __name__ == '__main__':
    app.run()
