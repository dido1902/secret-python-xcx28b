from flask import Blueprint

bp = Blueprint('loan', __name__)

from app.loan import routes