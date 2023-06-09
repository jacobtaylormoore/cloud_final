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
import error_handlers.error_handlers as error_handlers
from error_handlers.error_handlers import AuthError
from auth.jwt_handler import verify_jwt
import models.user as user_model

import src.constants as constants

client = datastore.Client()

app = Flask(__name__)
app.register_blueprint(boat.bp)
app.register_blueprint(user.bp)
app.register_blueprint(load.bp)
app.register_blueprint(error_handlers.bp)

app.secret_key = constants.SECRET_KEY
CLIENT_ID = constants.CLIENT_ID
CLIENT_SECRET = constants.CLIENT_SECRET
DOMAIN = constants.DOMAIN

ALGORITHMS = ["RS256"]

oauth = OAuth(app)

auth0 = oauth.register(
    'auth0',
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    client_kwargs={
        'scope': 'openid profile email',
    },
    server_metadata_url=f'https://{DOMAIN}/.well-known/openid-configuration',
)


@app.route("/")
def home():
    # temp = session.get(("user"), indent=4)
    query = client.query(kind="User")
    info = list(query.fetch())
    temp = json.dumps(session.get("user"), indent=4)

    return render_template(
        "home.html",
        session=session.get("user"),
        pretty=temp,
    )


@app.route('/decode', methods=['GET'])
def decode_jwt():
    payload = verify_jwt(request)
    return payload


@app.route("/callback", methods=["GET", "POST"])
def callback():
    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    user = user_model.User(token["userinfo"]["sub"],
                           token["userinfo"]["nickname"],
                           [])
    user.save_if_new()
    # user_key = client.key("User")
    # user = datastore.Entity(key=user_key)
    # user.update(
    #     {
    #         "user_id": token["userinfo"]["sub"],
    #         "boats": [],
    #         "name": token["userinfo"]["nickname"]
    #     }
    # )
    # client.put(user)
    return redirect("/")


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return oauth.auth0.authorize_redirect(
            redirect_uri=url_for("callback", _external=True)
        )
    elif request.method == 'POST':
        content = request.get_json()
        username = content["username"]
        password = content["password"]
        body = {'grant_type': 'password', 'username': username,
                'password': password,
                'client_id': CLIENT_ID,
                'client_secret': CLIENT_SECRET
                }
        headers = {'content-type': 'application/json'}
        url = 'https://' + DOMAIN + '/oauth/token'
        r = requests.post(url, json=body, headers=headers)
        return r.text, 200, {'Content-Type': 'application/json'}


@app.route("/logout")
def logout():
    session.clear()
    return redirect(
        "https://"
        + DOMAIN
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("home", _external=True),
                "client_id": CLIENT_ID,
            },
            quote_via=quote_plus,
        )
    )


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
