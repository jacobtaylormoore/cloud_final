
from flask import Flask, Blueprint, request, make_response
from google.cloud import datastore
import json
import src.constants as constants
from auth.jwt_handler import verify_jwt, verify_jwt_no_errors
import models.user as user_model
from error_handlers.error_handlers import raise_error

client = datastore.Client()

bp = Blueprint('user', __name__, url_prefix='/users')


@bp.route('', methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def users_get():
    if request.method == 'GET':
        return user_model.get_all_users(), 200
    else:
        return raise_error(405)
