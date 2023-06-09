
from flask import Flask, Blueprint, request, make_response
from google.cloud import datastore
import json
from auth.jwt_handler import verify_jwt, verify_jwt_no_errors
import models.boat as boat_model
import src.constants as constants
from error_handlers.error_handlers import raise_error

client = datastore.Client()

bp = Blueprint('boat', __name__, url_prefix='/boats')


@bp.route('', methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def boats_get_post():
    try:
        payload = verify_jwt(request)
        sub = payload["sub"]
    except:
        return raise_error(401)

    if request.method == 'GET':
        return boat_model.get_boats(sub, int(request.args.get('limit', '5')), int(request.args.get('offset', '0')), request.base_url), 200

    elif request.method == 'POST':
        try:
            content = request.get_json()
            boat = boat_model.Boat(
                content["name"], content["type"], content["length"], content["loads"], sub)
            saved = boat.save_boat()
            return json.dumps(saved), 201
        except:
            return raise_error(400)

    else:
        return raise_error(405)


@bp.route('/<boat_id>', methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def boat_get_delete_edit(boat_id):
    boat, boat_key = boat_model.get_boat_from_id(boat_id)
    if boat_key == -1:
        return raise_error(boat)
    try:
        payload = verify_jwt(request)
        sub = payload["sub"]
    except:
        return raise_error(401)

    if request.method == 'GET':
        if boat["owner"] != sub:
            return raise_error(403)
        else:
            return boat, 200

    elif request.method == 'DELETE':
        print(boat["owner"])
        print(sub)
        if boat["owner"] != sub:
            return raise_error(403)
        else:
            boat_model.delete_boat(boat_id, sub)
            return {}, 204

    elif request.method == 'PUT':
        pass

    else:
        return raise_error(405)
