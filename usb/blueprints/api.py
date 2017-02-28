from flask import Blueprint, jsonify, request

from usb.models import db, Redirect, DeviceType
from usb.shortener import get_short_id, get_short_url

api = Blueprint('api', __name__)


@api.route('/links')
def get_links():
    return jsonify({}), 200


@api.route('/links', methods=['POST'])
def shorten_url():
    short_id = get_short_id()
    long_url = request.json['url']
    for device_type in DeviceType:
        db.session.add(Redirect(short_id, device_type, long_url))
    db.session.commit()
    short_url = get_short_url(short_id)
    return jsonify(url=short_url), 200
