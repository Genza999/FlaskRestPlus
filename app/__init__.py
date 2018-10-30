# app/__init__.py

from flask_restplus import Api
from flask import Blueprint

from .main.controller.app_controller import api as inventory_ns

blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          title='SAYUNI API DOCUMENTATION',
          version='1.0',
          description='Documentation for Sayuni Hardware Api '
          )

api.add_namespace(inventory_ns, path='/inventory')
