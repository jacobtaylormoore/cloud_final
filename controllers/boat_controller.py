from flask import Flask, Blueprint, request, make_response
from google.cloud import datastore
import json
import src.old_constants as old_constants
from src.old_main import verify_jwt, verify_jwt_no_errors, app

client = datastore.Client()
app = Flask(__name__)
# bp = Blueprint('boats', __name__, url_prefix='/boats')


@app.route('/boats', methods=['POST', 'GET'])
def boats_get_post():
    if request.method == 'POST':
        try:
            payload = verify_jwt(request)
            content = request.get_json()
            new_boat = datastore.entity.Entity(
                key=client.key(old_constants.boats))
            new_boat.update(
                {"name": content["name"], "type": content["type"], "length": int(content["length"]), "public": content["public"], "owner": payload["sub"]})
            client.put(new_boat)
            boat_key = client.key(old_constants.boats, new_boat.key.id)
            boat = client.get(key=boat_key)
            boat["id"] = new_boat.key.id
            boat["self"] = old_constants.app_url + \
                '/boats/' + str(new_boat.key.id)
            return json.dumps(boat), 201
        except:
            response = {
                "Error": "The jwt is missing or not valid."
            }
            return response, 401
    elif request.method == 'GET':
        payload, jwt_valid = verify_jwt_no_errors(request)
        query = client.query(kind=old_constants.boats)
        if not jwt_valid:
            query.add_filter("public", "=", True)
        else:
            query.add_filter("owner", "=", payload["sub"])
        results_list = list(query.fetch())
        for e in results_list:
            e["id"] = e.key.id
        return json.dumps(results_list), 200
    else:
        return 'Method not recognized', 400


###########################
###########################


@app.route('/boats/deleteall', methods=['DELETE'])
def delete_all():
    query = client.query(kind=old_constants.boats)
    results_list = list(query.fetch())
    for e in results_list:
        # e["id"] = e.key.id
        client.delete(e.key)
    query = client.query(kind=old_constants.boats)
    new_list = list(query.fetch())
    print(results_list)
    print(new_list)
    return {}, 204


###########################
###########################


@app.route('/boats/<boat_id>', methods=['GET', 'DELETE'])
def boats_get_delete(boat_id):
    boat, boat_key = get_boat_from_id(boat_id)
    if request.method == 'GET':
        try:
            boat["id"] = boat_id
            boat["self"] = old_constants.app_url + '/boats/' + str(boat_id)
        except:
            response = {"Error": "No boat with this boat_id exists"}
            return response, 404
    elif request.method == 'DELETE':
        payload = verify_jwt(request)
        boat, boat_key = get_boat_from_id(boat_id)
        if boat is None:
            return {}, 403
        if payload["sub"] == boat["owner"]:
            client.delete(boat_key)
            return {}, 204
        else:
            return {}, 403

    else:
        return 'Method not recognized'


###########################
###########################


@app.route('/owners/<owner_id>/boats', methods=['GET'])
def boats_get_from_owner(owner_id):
    query = client.query(kind=old_constants.boats)
    query.add_filter("owner", "=", owner_id)
    query.add_filter("public", "=", True)
    results_list = list(query.fetch())
    return results_list, 200

###########################
###########################


# Retrieves boat object from db
def get_boat_from_id(boat_id):
    boat_key = client.key(old_constants.boats, int(boat_id))
    return client.get(key=boat_key), boat_key


# Return input boat formatted for html
def html_boat(boat):
    return '<ul>' + boat["name"] + \
        '<li>' + boat["id"] + '</li>' + \
        '<li>' + boat["type"] + '</li>' + \
        '<li>' + str(boat["length"]) + '</li>' + \
        '<li>' + boat["self"] + '</li>' + '</ul>'
