
from flask import Flask, Blueprint, request, make_response
from google.cloud import datastore
import json
import src.constants as constants
from auth.jwt_handler import verify_jwt, verify_jwt_no_errors

client = datastore.Client()

bp = Blueprint('user', __name__, url_prefix='/users')


@bp.route('', methods=['GET'])
def users_get():
    if request.method == 'GET':
        query = client.query(kind=constants.users)
        results_list = list(query.fetch())
        return json.dumps(results_list), 200
    else:
        return 'Method not recognized', 400
