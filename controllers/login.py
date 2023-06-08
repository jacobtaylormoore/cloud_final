from google.cloud import datastore
from flask import Flask, Blueprint, redirect, render_template, request, jsonify, session, url_for, _request_ctx_stack
import requests
from urllib.parse import quote_plus, urlencode

from functools import wraps
import json

from flask_cors import cross_origin
from jose import jwt

from six.moves.urllib.request import urlopen
import json
from os import environ as env
from werkzeug.exceptions import HTTPException

from authlib.integrations.flask_client import OAuth

import src.constants as constants

client = datastore.Client()

bp = Blueprint('login', __name__, url_prefix='/login')
