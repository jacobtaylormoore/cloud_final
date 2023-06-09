from flask import jsonify, Blueprint

bp = Blueprint('error_handlers', __name__)


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


@bp.app_errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response


def raise_error(code):
    if code == 400:
        return {"Error": "The request object is missing at least one of the required attributes."}, 400
    elif code == 401:
        return {"Error": "The jwt is missing or not valid."}, 401
    elif code == 403:
        return {"Error": "The user does not have permission for this."}, 403
    elif code == 404:
        return {"Error": "The requested entity was not found."}, 404
    elif code == 405:
        return {"Error": "Method not allowed"}, 405
    elif code == 406:
        return {"Error": "Cannot produce acceptable response body."}, 406
