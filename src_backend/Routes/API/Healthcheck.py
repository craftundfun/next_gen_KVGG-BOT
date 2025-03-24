from flask import Blueprint, jsonify

healthcheckBp = Blueprint('healthcheck', __name__)


@healthcheckBp.route('/health')
def healthcheck():
    return jsonify(
        {
            "status": "ok",
        }
    ), 200
