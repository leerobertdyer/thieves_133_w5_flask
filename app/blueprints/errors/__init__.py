from flask import Blueprint

errors = Blueprint('errors', __name__, template_folder='errors_templates')

from . import routes