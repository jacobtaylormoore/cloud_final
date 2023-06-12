
from flask import Flask, Blueprint, request, make_response
from google.cloud import datastore
import json
import models.load as load_model
import src.constants as constants
from error_handlers.error_handlers import raise_error
import models.boat as boat_model
from auth.jwt_handler import validate_mime

client = datastore.Client()

bp = Blueprint('load', __name__, url_prefix='/loads')


@bp.route('', methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def loads_get_post():
    if validate_mime(request) == 406:
        return raise_error(406)
    if request.method == 'POST':
        try:
            content = request.get_json()
            if len(dict.keys(content)) > 3:
                return raise_error(400)
            if 'carrier' in dict.keys(content):
                load = load_model.Load(
                    volume=content["volume"], description=content["description"], carrier=content["carrier"])
                saved = load.create_new_load()
            else:
                load = load_model.Load(
                    volume=content["volume"], description=content["description"])
                saved = load.create_new_load()
            if saved == 404:
                return raise_error(404)
            return saved, 201
        except:
            return raise_error(400)

    elif request.method == 'GET':
        return load_model.get_loads(int(request.args.get('limit', '5')), int(request.args.get('offset', '0')), request.base_url), 200

    else:
        return raise_error(405)


@bp.route('/<load_id>', methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def load_get_delete_put_patch(load_id):
    if not load_id:
        return raise_error(400)
    load, load_key = load_model.get_load_from_id(load_id)
    if load_key == -1:
        return raise_error(load)

    if request.method == 'GET':
        if validate_mime(request) == 406:
            return raise_error(406)
        return json.dumps(load), 200

    elif request.method == 'DELETE':
        response = load_model.delete_load(load_id)
        if response == 204:
            return {}, 204
        else:
            return raise_error(404)

    elif request.method == 'PUT':
        if validate_mime(request) == 406:
            return raise_error(406)
        try:
            content = request.get_json()
            load_obj = load_model.get_load_obj(load_id)
            if load_obj == 404:
                return raise_error(404)
            put = load_obj.put_load(
                load_id=int(load_id), volume=content["volume"], description=content["description"])
            if put == 404:
                return raise_error(404)
            return json.dumps(put), 200
        except:
            return raise_error(400)

    elif request.method == 'PATCH':
        if validate_mime(request) == 406:
            return raise_error(406)
        try:
            content = request.get_json()
            load_obj = load_model.get_load_obj(load_id)
            keys = list(dict.keys(content))
            if len(keys) > 2:
                return raise_error(400)
            test_keys = ['volume', 'description']
            # Vals contains values to send to user.patch_boat(). If none, value was not sent
            # Values sent to patch_boat as none will not be changed
            vals = [None, None]
            for key in keys:
                if key == test_keys[0]:
                    vals[0] = content["volume"]
                elif key == test_keys[1]:
                    vals[1] = content["description"]
                else:
                    return raise_error(400)

            patch = load_obj.patch_load(
                int(load_id), volume=vals[0], description=vals[1])
            if patch == 404:
                return raise_error(404)
            return json.dumps(patch), 200

        except:
            return raise_error(400)

    else:
        return raise_error(405)


@bp.route('/<load_id>/boats/<boat_id>', methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def load_add_remove_carrier(load_id, boat_id):
    if not load_id or not boat_id:
        return raise_error(400)
    boat, boat_key = boat_model.get_boat_from_id(int(boat_id))
    if boat_key == -1:
        return raise_error(boat)
    load, load_key = load_model.get_load_from_id(int(load_id))
    if load_key == -1:
        return raise_error(load)

    if request.method == 'PUT':
        boat_obj = boat_model.get_boat_obj(int(boat_id))
        boat_obj.add_load(int(load_id), int(boat_id))
        return {}, 200

    elif request.method == 'DELETE':
        load_obj = load_model.get_load_obj(int(load_id))
        load_obj.remove_carrier(int(load_id))
        return {}, 204

    else:
        return raise_error(405)
