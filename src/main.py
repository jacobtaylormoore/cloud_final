from google.cloud import datastore
from flask import Flask, redirect, render_template, request, jsonify, session, url_for, _request_ctx_stack
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
import controllers.boat_controller as boat
import controllers.user_controller as user
import controllers.load_controller as load

import constants

app = Flask(__name__)
app.register_blueprint(boat.bp)
app.register_blueprint(user.bp)
app.register_blueprint(load.bp)


@app.route("/")
def home():
    return render_template(
        "home.html",
        session=session.get("user"),
        pretty=json.dumps(session.get("user"), indent=4),
    )
