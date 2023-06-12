from google.cloud import datastore
import json
from error_handlers.error_handlers import raise_error
import src.constants as constants
import models.user as user_model
import models.load as load_model

client = datastore.Client()


class Boat:

    def __init__(self, name, type, length, owner, loads=[]):
        self.name = name
        self.type = type
        self.length = length
        self.loads = loads
        self.owner = owner

    def __str__(self):
        return "Name: " + self.name + "\n" + "type: " + self.type + "\n" + "length: " + str(self.length) + "\n" + "loads: " + str(self.loads) + "\n" + "owner: " + self.owner + "\n"

    def get_loads(self):
        return self.loads

    # Save boat to db
    def save_boat(self):
        new_boat = datastore.Entity(key=client.key(constants.boats))
        if self.loads:
            valid_loads = load_model.validate_loads(self.loads)
            if not valid_loads:
                return 400
        new_boat.update({"name": self.name, "type": self.type,
                        "length": self.length, "loads": self.loads, "owner": self.owner})
        client.put(new_boat)
        for load in self.loads:
            load_obj = load_model.get_load_obj(int(load))
            load_obj.add_carrier(int(new_boat.key.id), int(load))
        boat_key = client.key(constants.boats, new_boat.key.id)
        boat = client.get(key=boat_key)
        boat["id"] = new_boat.key.id
        boat["self"] = constants.app_url + '/boats/' + str(new_boat.key.id)

        # Now add boat id to user "boats"
        user = user_model.get_user_by_id(self.owner)

        user.add_new_boat(boat["id"])

        return boat

    # Edit boat (put)
    def put_boat(self, boat_id, name, type, length):
        boat_key = client.key(constants.boats, int(boat_id))
        boat = client.get(key=boat_key)
        if boat is None:
            return 404
        boat.update(
            {
                "name": name,
                "type": type,
                "length": length,
                "loads": self.loads,
                "owner": self.owner
            }
        )
        client.put(boat)
        boat["id"] = int(boat_id)
        boat["self"] = constants.app_url + '/boats/' + str(boat_id)
        return boat

    # Edit boat (patch)
    def patch_boat(self, boat_id, name, type, length):
        boat_key = client.key(constants.boats, int(boat_id))
        boat = client.get(key=boat_key)
        if boat is None:
            return 404
        if name:
            self.name = name
        if type:
            self.type = type
        if length:
            self.length = length
        boat.update(
            {
                "name": self.name,
                "type": self.type,
                "length": self.length,
                "loads": self.loads,
                "owner": self.owner
            }
        )
        client.put(boat)
        boat["id"] = int(boat_id)
        boat["self"] = constants.app_url + '/boats/' + str(boat_id)
        return boat

    # Add load to boat
    def add_load(self, load_id, boat_id):
        if int(load_id) in self.loads:
            return get_boat_from_id(boat_id=boat_id)
        self.loads.append(int(load_id))
        load = load_model.get_load_obj(int(load_id))
        load.add_carrier(int(boat_id), int(load_id))
        return self.patch_boat(boat_id=boat_id, name=None, type=None, length=None)

    # Remove load from boat
    def remove_load(self, load_id, boat_id):
        if int(load_id) not in self.loads:
            return
        self.loads.remove(load_id)
        self.patch_boat(boat_id=boat_id, name=None, type=None,
                        length=None)
        # load = load_model.get_load_obj(int(load_id))
        # if load == 404:
        #     return
        # load.remove_carrier(int(load_id))
        return

    # Update loads by going through old array of load_ids and comparing to new
    # array of load_ids
    def update_loads(self, boat_id, old_loads, new_loads):
        # First, remove old loads that are no longer in loads array
        for load in old_loads:
            if load not in new_loads:
                self.remove_load(int(load), int(boat_id))

        # Then add new loads
        for load in new_loads:
            if load not in old_loads:
                self.add_load(int(load), int(boat_id))


##############################################################################
##############################################################################


# Get boat from id
def get_boat_from_id(boat_id):
    boat_key = client.key(constants.boats, int(boat_id))
    boat = client.get(key=boat_key)
    if boat is None:
        return 404, -1
    else:
        boat["id"] = int(boat_id)
        boat["self"] = constants.app_url + '/boats/' + str(boat_id)
        return boat, boat_key


def get_boat_obj(boat_id):
    boat_key = client.key(constants.boats, int(boat_id))
    boat = client.get(key=boat_key)
    if boat is None:
        return 404
    else:
        ret_boat = Boat(boat["name"], boat["type"],
                        boat["length"], boat["owner"], boat["loads"])
        return ret_boat


def get_boats(owner_id, limit, offset, url):
    all, num = get_boats_no_pagination()
    query = client.query(kind=constants.boats)
    query.add_filter("owner", "=", owner_id)
    q_limit = limit
    q_offset = offset
    g_iterator = query.fetch(limit=q_limit, offset=q_offset)
    pages = g_iterator.pages
    results = list(next(pages))
    if g_iterator.next_page_token:
        next_offset = q_offset + q_limit
        next_url = url + '?limit=' + \
            str(q_limit) + '&offset=' + str(next_offset)
    else:
        next_url = None
    for e in results:
        e["id"] = e.key.id
    output = {"boats": results}
    output["num_boats"] = num
    if next_url:
        output["next"] = next_url
    return json.dumps(output)


def get_boats_no_pagination():
    query = client.query(kind=constants.boats)
    results = list(query.fetch())
    return results, len(results)


def get_all_boats():
    query = client.query(kind=constants.boats)
    results = list(query.fetch())
    return json.dumps(results)


def delete_boat(boat_id, user_id):
    user = user_model.get_user_obj(user_id)
    if user == 404:
        return raise_error(404)
    user.remove_boat(int(boat_id))
    boat, boat_key = get_boat_from_id(boat_id)
    if boat == 404:
        return raise_error(404)
    else:
        for load in boat["loads"]:
            load_obj = load_model.get_load_obj(int(load))
            load_obj.remove_carrier(int(load))
        client.delete(boat_key)
        return {}, 204

    ####################################
    # For testing purposes
    ####################################


def delete_all_boats():
    query = client.query(kind=constants.boats)
    results = list(query.fetch())
    for e in results:
        boat_id = e.key.id
        boat = get_boat_obj(int(boat_id))
        boat.update_loads(int(boat_id), boat.loads, [])
        client.delete(e.key)
    user_model.remove_all_boats()
    return
