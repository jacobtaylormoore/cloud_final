import models.user as user
import models.boat as boat
import models.load as load
import unittest
import os

# print(user.get_all_users())
# print(boat.get_all_boats())
# user.delete_all_users()
boat.delete_all_boats()
print(user.get_all_users())
load.delete_all_loads()
# print(boat.get_all_boats())
# print('\n\n')
# print(user.get_all_users())
# print('\n\n')
# print(user.user_test(123))
# user_id = "auth0|647a5330f0c4adc889598267"
# print(user.get_user_by_id(user_id))
