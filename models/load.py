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
        return "Volume: " + str(self.volume) + "\n" + "Description: " + self.description + "\n" + "Carrier: " + str(self.carrier) + "Creation Date: " + self.creation_date + "\n"

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

    def patch_load(self, load_id, volume, description, carrier):
        load_key = client.key(constants.loads, int(load_id))
        load = client.get(key=load_key)
        if load is None:
            return 404
        if volume:
            self.volume = volume
        if description:
            self.description = description
        if carrier:
            self.carrier = carrier

####################################
# update loads
####################################
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
    if next_url:
        output["next"] = next_url
    return json.dumps(output)


def delete_all_loads():
    ###########
    # Will need to update when connection with boats added
    ###########
    query = client.query(kind=constants.loads)
    results = list(query.fetch())
    for e in results:
        delete_load(e["id"])
    return
