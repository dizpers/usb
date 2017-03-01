from collections import defaultdict

from flask import Blueprint, jsonify, request

from usb.models import db, Redirect, DeviceType
from usb.shortener import get_short_id, get_short_url

api = Blueprint('api', __name__)


@api.route('/urls')
def get_list_of_urls():
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


@api.route('/urls', methods=['POST'])
def create_short_url():
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


@api.route('/urls/<string:short_id>', methods=['PATCH'])
def update_short_url(short_id):
    data = request.json
    redirect = Redirect.query.filter_by(short=short_id).first()
    if redirect is None:
        return jsonify({}), 404
    for key in data:
        Redirect.query.filter_by(short=short_id, type=DeviceType[key.upper()]).update({'url': data[key]})
    if data:
        db.session.commit()
    return jsonify({}), 200
