
from flask import Flask, Blueprint, request, make_response
from google.cloud import datastore
import json
import src.constants as constants

client = datastore.Client()

bp = Blueprint('boat', __name__, url_prefix='/boats')

# @bp.route('', methods=['GET'])
