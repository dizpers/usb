from collections import defaultdict

from flask import Blueprint, jsonify, request, redirect, current_app

from usb.models import db, Redirect, Desktop, Tablet, Mobile
from usb.shortener import get_short_id, get_short_url
from usb.utils import get_device_model_from_code, get_device_model_from_request

api = Blueprint('api', __name__)


@api.route('/urls')
def get_list_of_urls():
    redirects = Redirect.query.all()
    result = defaultdict(list)
    for redirect in redirects:
        result[redirect.short].append({
            'type': redirect.type,
            'url': redirect.url,
            'redirects': redirect.count,
            'datetime': redirect.datetime
        })
    return jsonify(result), 200


@api.route('/urls', methods=['POST'])
def create_short_url():
    short_id = get_short_id()
    long_url = request.json['url']
    db.session.add(Desktop(short_id, long_url))
    db.session.add(Tablet(short_id, long_url))
    db.session.add(Mobile(short_id, long_url))
    db.session.commit()
    short_url = get_short_url(short_id)
    return jsonify(url=short_url), 200


@api.route('/urls/<string:short_id>', methods=['PATCH'])
def update_short_url(short_id):
    data = request.json
    if Redirect.query.filter_by(short=short_id).first() is None:
        return jsonify({}), 404
    for key in data:
        device_model = get_device_model_from_code(key)
        db.session.delete(device_model.query.filter_by(short=short_id).first())
        db.session.add(device_model(short_id, data[key]))
    if data:
        db.session.commit()
    return jsonify({}), 200


@api.route('/<string:short_id>')
@api.route('/urls/<string:short_id>')
def redirect_from_short_url(short_id):
    device_model = get_device_model_from_request(request)
    redirect_instance = device_model.query.filter_by(short=short_id).first()
    if redirect_instance is None:
        return jsonify({}), 404
    redirect_instance.count += 1
    db.session.commit()
    return redirect(redirect_instance.url, current_app.config['REDIRECT_CODE'])
