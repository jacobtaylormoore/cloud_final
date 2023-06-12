
from flask import Flask, Blueprint, request, make_response
from google.cloud import datastore
import json
from auth.jwt_handler import verify_jwt, validate_mime
import models.boat as boat_model
import src.constants as constants
from error_handlers.error_handlers import raise_error

client = datastore.Client()

bp = Blueprint('boat', __name__, url_prefix='/boats')


@bp.route('', methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def boats_get_post():
    if validate_mime(request) == 406:
        return raise_error(406)
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
            keys = dict.keys(content)
            if len(keys) > 4:
                return raise_error(400)
            if "loads" in keys and content["loads"]:
                return raise_error(400)
            boat = boat_model.Boat(
                content["name"], content["type"], content["length"], sub)
            saved = boat.save_boat()
            if saved == 400:
                return raise_error(400)
            return json.dumps(saved), 201
        except:
            return raise_error(400)

    else:
        return raise_error(405)


@bp.route('/<boat_id>', methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def boat_get_delete_edit(boat_id):
    if not boat_id:
        return raise_error(400)
    boat, boat_key = boat_model.get_boat_from_id(boat_id)
    if boat_key == -1:
        return raise_error(boat)
    try:
        payload = verify_jwt(request)
        sub = payload["sub"]
    except:
        return raise_error(401)

    if request.method == 'GET':
        if validate_mime(request) == 406:
            return raise_error(406)
        if boat["owner"] != sub:
            return raise_error(403)
        else:
            return boat, 200

    elif request.method == 'DELETE':
        if boat["owner"] != sub:
            return raise_error(403)
        else:
            boat_model.delete_boat(boat_id, sub)
            return {}, 204

    elif request.method == 'PUT':
        if validate_mime(request) == 406:
            return raise_error(406)
        if boat["owner"] != sub:
            return raise_error(403)
        # Check that request contains all variables to update
        try:
            content = request.get_json()
            keys = dict.keys(content)
            if len(keys) > 4:
                return raise_error(400)
            if "loads" in keys and content["loads"]:
                return raise_error(400)
            boat = boat_model.get_boat_obj(boat_id)
            put = boat.put_boat(int(boat_id), content["name"], content["type"],
                                content["length"])
            if put == 400:
                return raise_error(400)
            if put == 404:
                return raise_error(404)
            return json.dumps(put), 200
        except:
            return raise_error(400)

    elif request.method == 'PATCH':
        if validate_mime(request) == 406:
            return raise_error(406)
        if boat["owner"] != sub:
            return raise_error(403)
        try:
            content = request.get_json()
            keys = dict.keys(content)
            if len(keys) > 3:
                return raise_error(400)
            if "loads" in keys:
                return raise_error(400)
            boat = boat_model.get_boat_obj(boat_id)
            keys = list(dict.keys(content))
            test_keys = ["name", "type", "length"]
            # Vals contains values to send to user.patch_boat(). If none, value was not sent
            # Values sent to patch_boat as none will not be changed
            vals = [None, None, None]
            for key in keys:
                if key not in test_keys:
                    return raise_error(400)
                if key == test_keys[0]:
                    vals[0] = content["name"]
                elif key == test_keys[1]:
                    vals[1] = content["type"]
                elif key == test_keys[2]:
                    vals[2] = content["length"]
                else:
                    return raise_error(400)
            patch = boat.patch_boat(boat_id=int(
                boat_id), name=vals[0], type=vals[1], length=vals[2])
            if patch == 404:
                return raise_error(404)
            if patch == 400:
                return raise_error(400)
            return json.dumps(patch), 200
        except:
            return raise_error(400)

    else:
        return raise_error(405)
