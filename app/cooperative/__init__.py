from flask import Blueprint

bp = Blueprint('cooperative', __name__)

from app.cooperative import routes