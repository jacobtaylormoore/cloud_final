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
import controllers.boat_controller as boat_controller
# from jwt_handler import verify_jwt, CLIENT_ID, CLIENT_SECRET, DOMAIN
import src.old_constants as old_constants

app = Flask(__name__)
app.secret_key = 'SECRET_KEY'
# app.register_blueprint(boat.bp)
client = datastore.Client()

ALGORITHMS = ["RS256"]

# Update the values of the following 3 variables
CLIENT_ID = '97byC11AB5Q1DFk3WgI9g4mIR2cPDCm9'
CLIENT_SECRET = 'IwLA0xWS6YmpmwKy4qRSsAA_-xMMnV2h5vf87vvy2hMOuNsdkLVLbdF7VtWchFzS'
DOMAIN = 'mooreja2-jwt.us.auth0.com'
# For example
# DOMAIN = 'fall21.us.auth0.com'

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


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


@app.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response


def verify_jwt_no_errors(request):
    if 'Authorization' in request.headers:
        auth_header = request.headers['Authorization'].split()
        token = auth_header[1]
    else:
        return ({"code": "no auth header",
                         "description":
                 "Authorization header is missing"}, False)

    jsonurl = urlopen("https://" + DOMAIN+"/.well-known/jwks.json")
    jwks = json.loads(jsonurl.read())
    try:
        unverified_header = jwt.get_unverified_header(token)
    except jwt.JWTError:
        return ({"code": "invalid_header",
                 "description":
                 "Invalid header. "
                 "Use an RS256 signed JWT Access Token"}, False)
    if unverified_header["alg"] == "HS256":
        return ({"code": "invalid_header",
                 "description":
                 "Invalid header. "
                 "Use an RS256 signed JWT Access Token"}, False)
    rsa_key = {}
    for key in jwks["keys"]:
        if key["kid"] == unverified_header["kid"]:
            rsa_key = {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key["use"],
                "n": key["n"],
                "e": key["e"]
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=CLIENT_ID,
                issuer="https://" + DOMAIN+"/"
            )
        except Exception:
            return ({"code": "invalid_header",
                     "description":
                     "Unable to parse authentication"
                     " token."}, False)

        return (payload, True)
    else:
        return ({"code": "no_rsa_key",
                         "description":
                 "No RSA key in JWKS"}, False)


def verify_jwt(request):
    if 'Authorization' in request.headers:
        auth_header = request.headers['Authorization'].split()
        token = auth_header[1]
    else:
        raise AuthError({"code": "no auth header",
                         "description":
                         "Authorization header is missing"}, 401)

    jsonurl = urlopen("https://" + DOMAIN+"/.well-known/jwks.json")
    jwks = json.loads(jsonurl.read())
    try:
        unverified_header = jwt.get_unverified_header(token)
    except jwt.JWTError:
        raise AuthError({"code": "invalid_header",
                        "description":
                            "Invalid header. "
                            "Use an RS256 signed JWT Access Token"}, 401)
    if unverified_header["alg"] == "HS256":
        raise AuthError({"code": "invalid_header",
                        "description":
                            "Invalid header. "
                            "Use an RS256 signed JWT Access Token"}, 401)
    rsa_key = {}
    for key in jwks["keys"]:
        if key["kid"] == unverified_header["kid"]:
            rsa_key = {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key["use"],
                "n": key["n"],
                "e": key["e"]
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=CLIENT_ID,
                issuer="https://" + DOMAIN+"/"
            )
        except jwt.ExpiredSignatureError:
            raise AuthError({"code": "token_expired",
                            "description": "token is expired"}, 401)
        except jwt.JWTClaimsError:
            raise AuthError({"code": "invalid_claims",
                            "description":
                                "incorrect claims,"
                                " please check the audience and issuer"}, 401)
        except Exception:
            raise AuthError({"code": "invalid_header",
                            "description":
                                "Unable to parse authentication"
                                " token."}, 401)

        return payload
    else:
        raise AuthError({"code": "no_rsa_key",
                         "description":
                         "No RSA key in JWKS"}, 401)


# Controllers API
@app.route("/")
def home():
    return render_template(
        "home.html",
        session=session.get("user"),
        pretty=json.dumps(session.get("user"), indent=4),
    )


@app.route('/decode', methods=['GET'])
def decode_jwt():
    payload = verify_jwt(request)
    return payload


@app.route("/callback", methods=["GET", "POST"])
def callback():
    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    return redirect("/")


@app.route("/login")
def login():
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True)
    )


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
