
from flask import Blueprint, request
from google.cloud import datastore
from auth.jwt_handler import validate_mime
import models.user as user_model
from error_handlers.error_handlers import raise_error

client = datastore.Client()

bp = Blueprint('user', __name__, url_prefix='/users')


@bp.route('', methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def users_get():
    if request.method == 'GET':
        if validate_mime(request) == 406:
            return raise_error(406)
        return user_model.get_all_users(), 200
    else:
        return raise_error(405)
