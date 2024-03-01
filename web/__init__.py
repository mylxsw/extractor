from flask import Blueprint
from flask_restful import Api

bp = Blueprint('web', __name__, url_prefix='/v1')
api = Api(bp)

from . import extractor
