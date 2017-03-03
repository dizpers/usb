from collections import defaultdict

from flask import Blueprint, jsonify, request, redirect, current_app

from usb.models import db, Redirect, DesktopRedirect, TabletRedirect, MobileRedirect
from usb.utils import get_device_model_from_string, get_device_model_from_request

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
    """
    Besides the approach used here, other options were also considered. Among them are
    the following ones:

    1) use external sequence generator instead of auto-incremented PK (Primary Key)
    (like sequence generator in PosgreSQL, auto-incremented value in Redis and so on);

    2) usage of `parent_id` as a FK (Foreign Key) instead of `short` attribute;

    3) replace Single Table Inheritance approach with Class Table Inheritance;

    4) use base model as the source of PK, create FK to that model.

    The main reason of choice made in favor of implementation presented here is performance.
    Selected solution allows to avoid decoding on each API request. And, comparing to Class
    Table Inheritance, it avoids JOINs usage while getting data. The drawback of chosen method
    is the lack of integrity control. At the same time, it doesn't supported by SQLite and not
    required by business side - all connected values removed by value of `short` attribute, which
    makes integrity control not demanded.
    """
    long_url = request.json['url']
    desktop_redirect = DesktopRedirect('', long_url)
    db.session.add(desktop_redirect)
    db.session.commit()
    short_id = current_app.shortener.encode(desktop_redirect.id)
    desktop_redirect.short = short_id
    db.session.add(TabletRedirect(short_id, long_url))
    db.session.add(MobileRedirect(short_id, long_url))
    db.session.commit()
    short_url = f'http://{current_app.config["SHORT_URL_DOMAIN"]}/{short_id}'
    return jsonify(url=short_url), 200


@api.route('/urls/<string:short_id>', methods=['PATCH'])
def update_short_url(short_id):
    data = request.json
    if Redirect.query.filter_by(short=short_id).first() is None:
        return jsonify({}), 404
    for key in data:
        device_model = get_device_model_from_string(key)
        device_model.query.filter_by(short=short_id).delete()
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
    redirect_instance.increase_count()
    db.session.commit()
    return redirect(redirect_instance.url, current_app.config['REDIRECT_CODE'])
