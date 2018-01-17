from flask import Blueprint

sector = Blueprint('sector', __name__)

from . import views