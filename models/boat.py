from google.cloud import datastore
import json
import src.constants as constants
import models.user as user_model

client = datastore.Client()


class Boat:

    def __init__(self, name, type, length, loads, owner):
        self.name = name
        self.type = type
        self.length = length
        self.loads = loads
        self.owner = owner

    def __str__(self):
        return "Name: " + self.name + "\n" + "type: " + self.type + "\n" + "length: " + str(self.length) + "\n" + "loads: " + str(self.loads) + "\n" + "owner: " + self.owner + "\n"

    # Save boat to db
    def save_boat(self):
        new_boat = datastore.Entity(key=client.key(constants.boats))
        new_boat.update({"name": self.name, "type": self.type,
                        "length": self.length, "loads": self.loads, "owner": self.owner})
        client.put(new_boat)
        boat_key = client.key(constants.boats, new_boat.key.id)
        boat = client.get(key=boat_key)
        boat["id"] = new_boat.key.id
        boat["self"] = constants.app_url + '/boats/' + str(new_boat.key.id)

        # Now add boat id to user "boats"
        user = user_model.get_user_by_id(self.owner)
        user.add_new_boat(boat["id"])

        return boat

    # Edit boat (put)
    def put_boat(self, boat_id, name, type, length, loads):
        ####################################
        # update loads
        ####################################
        boat_key = client.key(constants.boats, int(boat_id))
        boat = client.get(key=boat_key)
        if boat is None:
            return 404
        boat.update(
            {
                "name": name,
                "type": type,
                "length": length,
                "loads": loads,
                "owner": self.owner
            }
        )
        client.put(boat)
        boat["id"] = int(boat_id)
        boat["self"] = constants.app_url + '/boats/' + str(boat_id)
        return boat

    # Edit boat (patch)
    def patch_boat(self, boat_id, name, type, length, loads):
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
        if loads:
            self.loads = loads
####################################
# update loads
####################################
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
        return self.patch_boat(boat_id=boat_id, name=None, type=None, length=None, loads=self.loads)

    # Remove load from boat
    def remove_load(self, load_id, boat_id):
        if int(load_id) not in self.loads:
            return
        self.loads.remove(load_id)
        self.patch_boat(boat_id=boat_id, name=None, type=None,
                        length=None, loads=self.loads)
        return

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
                        boat["length"], boat["loads"], boat["owner"])
        return ret_boat
# Get all boats of owner - jwt sub is user id


def get_boats(owner_id, limit, offset, url):
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
    if next_url:
        output["next"] = next_url
    return json.dumps(output)
    # results = list(query.fetch())
    # return json.dumps(results)

# Delete boat


def delete_boat(boat_id, user_id):
    ####################################
    # update loads
    ####################################
    user = user_model.get_user_by_id(user_id)
    user.remove_boat(int(boat_id))
    boat, boat_key = get_boat_from_id(boat_id)
    if boat == 404:
        return 404
    else:
        client.delete(boat_key)
        return 204


def delete_all_boats():
    ####################################
    # update loads
    ####################################
    query = client.query(kind=constants.boats)
    results = list(query.fetch())
    for e in results:
        client.delete(e.key)
    user_model.remove_all_boats()
    return


def get_all_boats():
    query = client.query(kind=constants.boats)
    results = list(query.fetch())
    return json.dumps(results)
