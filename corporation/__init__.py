from flask import Blueprint

corporation = Blueprint('corporation', __name__)

from . import views