from google.cloud import datastore
import json
import src.constants as constants

client = datastore.Client()


class User:

    def __init__(self, user_id, name, boats):
        self.user_id = user_id
        self.name = name
        self.boats = boats
        self.user_key = client.key(constants.users, user_id)

    def __str__(self):
        return "User id = " + str(self.user_id) + "\n" + "name = " + self.name + "\n" + "boats = " + str(self.boats)

    def save_if_new(self):
        user_exists = get_user_by_id(self.user_id)
        if not user_exists:
            user = datastore.Entity(key=self.user_key)
            user.update(
                {
                    "user_id": self.user_id,
                    "boats": self.boats,
                    "name": self.name
                }
            )
            client.put(user)
        return

    def add_new_boat(self, boat_id):
        self.boats.append(int(boat_id))
        self.update_table()
        return

    def remove_boat(self, boat_id):
        if int(boat_id) in self.boats:
            self.boats.remove(boat_id)
            self.update_table()
            return True
        else:
            return False

    def update_table(self):
        update_user = datastore.Entity(key=self.user_key)
        update_user.update(
            {
                "user_id": self.user_id,
                "boats": self.boats,
                "name": self.name
            }
        )
        client.put(update_user)
        return

    def remove_all_boats(self):
        self.boats = []
        self.update_table()
        return True


##############################################################################
##############################################################################


def get_user_by_id(user_id):
    query = client.query(kind=constants.users)
    query.add_filter("user_id", "=", user_id)
    results = list(query.fetch())
    if results:
        temp = results[0]
        user = User(temp["user_id"], temp["name"], temp["boats"])
    else:
        user = None
    return user


def get_user_obj(user_id):
    user_key = client.key(constants.users, user_id)
    user = client.get(key=user_key)
    if user is None:
        return 404
    else:
        ret_user = User(user["user_id"], user["name"], user["boats"])
        return ret_user


def get_all_users():
    query = client.query(kind=constants.users)
    results_list = list(query.fetch())
    return json.dumps(results_list)

    ####################################
    # For testing purposes
    ####################################


def delete_all_users():
    query = client.query(kind=constants.users)
    results_list = list(query.fetch())
    for e in results_list:
        client.delete(e.key)
    return


def remove_all_boats():
    query = client.query(kind=constants.users)
    users = list(query.fetch())
    for user in users:
        user_obj = get_user_obj(user["user_id"])
        user_obj.remove_all_boats()
    return
