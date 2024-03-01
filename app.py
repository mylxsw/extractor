import logging
from flask import Flask

import core.extensions.ext_storage as storage
from web import bp as web_bp

app = Flask(__name__)

app.register_blueprint(web_bp)
storage.init(storage.StorageConfig.local('/tmp'))

if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

if __name__ == '__main__':
    app.run()
