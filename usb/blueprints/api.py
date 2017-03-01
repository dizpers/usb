from collections import defaultdict

from flask import Blueprint, jsonify, request

from usb.models import db, Redirect, DeviceType
from usb.shortener import get_short_id, get_short_url

api = Blueprint('api', __name__)


@api.route('/links')
def get_links():
    # TODO: paginate?
    redirects = Redirect.query.all()
    result = defaultdict(list)
    for redirect in redirects:
        result[redirect.short].append({
            'type': redirect.type.name.lower(),
            'url': redirect.url,
            'redirects': redirect.count,
            # TODO: move to JSON serializer?
            'datetime': redirect.datetime.isoformat()
        })
    return jsonify(result), 200


@api.route('/links', methods=['POST'])
def shorten_url():
    short_id = get_short_id()
    long_url = request.json['url']
    redirect = Redirect.query.filter_by(url=long_url).first()
    if redirect:
        short_url = get_short_url(redirect.short)
        return jsonify(url=short_url), 409
    for device_type in DeviceType:
        db.session.add(Redirect(short_id, device_type, long_url))
    db.session.commit()
    short_url = get_short_url(short_id)
    return jsonify(url=short_url), 200
