from flask import Blueprint, jsonify

api = Blueprint('api', __name__)


@api.route('/links')
def get_links():
    return jsonify({}), 200
