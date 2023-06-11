
from flask import Flask, Blueprint, request, make_response
from google.cloud import datastore
import json
import models.load as load_model
import src.constants as constants
from error_handlers.error_handlers import raise_error

client = datastore.Client()

bp = Blueprint('load', __name__, url_prefix='/loads')


@bp.route('', methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def loads_get_post():
    if request.method == 'POST':
        try:
            content = request.get_json()
            load = load_model.Load(
                volume=content["volume"], description=content["description"])
            saved = load.create_new_load()
            return saved, 201
        except:
            return raise_error(400)

    elif request.method == 'GET':
        return load_model.get_loads(int(request.args.get('limit', '5')), int(request.args.get('offset', '0')), request.base_url), 200

    else:
        return raise_error(405)


@bp.route('/<load_id>', methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def load_get_delete_put_patch(load_id):
    load, load_key = load_model.get_load_from_id(load_id)
    if load_key == -1:
        return raise_error(load)

    if request.method == 'GET':
        return json.dumps(load), 200

    elif request.method == 'DELETE':
        response = load_model.delete_load(load_id)
        if response == 204:
            return {}, 204
        else:
            return raise_error(404)

    elif request.method == 'PUT':
        try:
            content = request.get_json()
            load_obj = load_model.get_load_obj(load_id)
            put = load_obj.put_load(
                load_id=int(load_id), volume=content["volume"], description=content["description"])
            if put == 404:
                return raise_error(404)
            return json.dumps(put), 200
        except:
            return raise_error(400)

    elif request.method == 'PATCH':
        try:
            content = request.get_json()
            load_obj = load_model.get_load_obj(load_id)
            keys = list(dict.keys(content))
            test_keys = ['volume', 'description', 'carrier']
            # Vals contains values to send to user.patch_boat(). If none, value was not sent
            # Values sent to patch_boat as none will not be changed
            vals = [None, None, None]
            for key in keys:
                if key == test_keys[0]:
                    vals[0] = content["volume"]
                elif key == test_keys[1]:
                    vals[1] = content["description"]
                elif key == test_keys[2]:
                    vals[2] = content["carrier"]
                else:
                    return raise_error(400)

#########################
# update boat
#########################

            patch = load_obj.patch_load(
                int(load_id), volume=vals[0], description=vals[1], carrier=vals[2])
            if patch == 404:
                return raise_error(404)
            return json.dumps(patch), 200

        except:
            return raise_error(400)

    else:
        return raise_error(405)
