
from flask import Flask, Blueprint, request, make_response
from google.cloud import datastore
import json
import src.constants as constants
from src.main import verify_jwt, verify_jwt_no_errors, app

client = datastore.Client()

bp = Blueprint('boat', __name__, url_prefix='/boats')

bp.route('', methods=['GET'])
