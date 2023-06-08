from google.cloud import datastore
import json
import src.constants as constants

client = datastore.Client()


class User:
    boats = []

    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name

    def save_if_new(self):
        user_exists = get_user_by_id(self.user_id)


def get_user_by_id(user_id):
    user_key = client.key(constants.users, int(user_id))
    user = client.get(key=user_key)
    # if user ==
    return True
