from collections import defaultdict

from flask import Blueprint, jsonify, request, redirect, current_app

from usb.models import db, Redirect, DeviceType
from usb.shortener import get_short_id, get_short_url
from usb.utils import get_device_type

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
        device_type = DeviceType[key.upper()]
        redirect = Redirect.query.filter_by(short=short_id, type=device_type).first()
        db.session.delete(redirect)
        db.session.add(Redirect(short_id, device_type, data[key]))
    if data:
        db.session.commit()
    return jsonify({}), 200


@api.route('/<string:short_id>')
@api.route('/urls/<string:short_id>')
def redirect_from_short_url(short_id):
    device_type = get_device_type(request)
    redirect_instance = Redirect.query.filter_by(short=short_id, type=device_type).first()
    if redirect_instance is None:
        return jsonify({}), 404
    return redirect(redirect_instance.url, current_app.config['REDIRECT_CODE'])
