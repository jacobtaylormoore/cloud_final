from google.cloud import datastore
import json
from datetime import date
from error_handlers.error_handlers import raise_error
import src.constants as constants
import models.boat as boat_model

client = datastore.Client()


class Load:

    def __init__(self, volume, description, carrier=None, creation_date=None):
        self.volume = volume
        self.description = description
        self.carrier = carrier
        self.creation_date = creation_date

    def __str__(self):
        return "Volume: " + str(self.volume) + "\n" + "Description: " + self.description + "\n" + "Carrier: " + str(self.carrier) + "\n" + "Creation Date: " + self.creation_date + "\n"

    def create_new_load(self):
        today = date.today()
        self.creation_date = today.strftime("%d/%m/%Y")
        load = datastore.Entity(key=client.key(constants.loads))
        load.update(
            {
                "volume": self.volume,
                "carrier": self.carrier,
                "description": self.description,
                "creation_date": self.creation_date
            }
        )
        client.put(load)
        load["id"] = load.key.id
        load["self"] = constants.app_url + '/loads/' + str(load["id"])
        return load

    def update_table(self, load_id):
        load_key = client.key(constants.loads, int(load_id))
        update_load = datastore.Entity(key=load_key)
        update_load.update(
            {
                "volume": self.volume,
                "carrier": self.carrier,
                "description": self.description,
                "creation_date": self.creation_date
            }
        )
        client.put(update_load)
        return update_load

    def put_load(self, load_id, volume, description):
        self.volume = volume
        self.description = description
        new_load = self.update_table(load_id=load_id)
        new_load["id"] = load_id
        new_load["self"] = constants.app_url + '/loads/' + str(load_id)
        return new_load

    def patch_load(self, load_id, volume, description):
        load_key = client.key(constants.loads, int(load_id))
        load = client.get(key=load_key)
        if load is None:
            return 404
        if volume:
            self.volume = volume
        if description:
            self.description = description
        load.update(
            {
                "volume": self.volume,
                "description": self.description,
                "carrier": self.carrier,
                "creation_date": self.creation_date
            }
        )
        client.put(load)
        load["id"] = int(load_id)
        load["self"] = constants.app_url + '/loads/' + str(load_id)
        return load

    def remove_carrier(self, load_id):
        if self.carrier:
            boat = boat_model.get_boat_obj(int(self.carrier))
            if boat == 404:
                return 404
            boat.remove_load(int(load_id), int(self.carrier))
        self.carrier = None
        self.update_table(int(load_id))
        return

    def add_carrier(self, boat_id, load_id):
        self.remove_carrier(int(load_id))
        self.carrier = int(boat_id)
        self.update_table(int(load_id))
        return


##############################################################################
##############################################################################


def get_load_from_id(load_id):
    load_key = client.key(constants.loads, int(load_id))
    load = client.get(key=load_key)
    if load is None:
        return 404, -1
    else:
        load["id"] = int(load_id)
        load["self"] = constants.app_url + '/loads/' + str(load_id)
        return load, load_key


def get_load_obj(load_id):
    load_key = client.key(constants.loads, int(load_id))
    load = client.get(key=load_key)
    if load is None:
        return 404
    else:
        ret_load = Load(load["volume"], load["description"],
                        load["carrier"], load["creation_date"])
        return ret_load


def delete_load(load_id):
    # Remove from boat
    load, load_key = get_load_from_id(int(load_id))
    if load_key == -1:
        return load
    if load["carrier"]:
        boat_id = load["carrier"]
        boat = boat_model.get_boat_obj(boat_id=int(boat_id))
        if boat != 404:
            boat.remove_load(int(load_id), int(boat_id))
    client.delete(load_key)
    return 204


# Function to remove boat_id from any loads being carried by said boat
def remove_carrier(boat_id):
    query = client.query(kind=constants.loads)
    query.add_filter("carrier", "=", int(boat_id))
    results_list = list(query.fetch())
    for load in results_list:
        update_load = get_load_obj(load.key.id)
        update_load["carrier"] = None
        update_load.update_table()
    return


def get_loads(limit, offset, url):
    all, num = get_loads_no_pagination()
    query = client.query(kind=constants.loads)
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
    output = {"loads": results}
    output["num_loads"] = num
    if next_url:
        output["next"] = next_url
    return json.dumps(output)


def get_loads_no_pagination():
    query = client.query(kind=constants.loads)
    results = list(query.fetch())
    return results, len(results)


def validate_loads(loads_array):
    results, num = get_loads_no_pagination()
    load_ids = []
    for e in results:
        load_ids.append(e.key.id)
    for load in loads_array:
        if int(load) not in load_ids:
            return False
    return True


def delete_all_loads():
    query = client.query(kind=constants.loads)
    results = list(query.fetch())
    for e in results:
        if e["carrier"]:
            boat = boat_model.get_boat_obj(int(e["carrier"]))
            if boat != 404:
                boat.remove_load(int(e.key.id), int(e["carrier"]))
        delete_load(int(e.key.id))
    return
