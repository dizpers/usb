from flask import Blueprint, jsonify

api = Blueprint('api', __name__)


@api.route('/links')
def get_links():
    return jsonify({}), 200


@api.route('/links', methods=['POST'])
def shorten_url():
    return jsonify({}), 200
