from flask import Blueprint

api_post = Blueprint('api_post', __name__)

from app.api_post import views
