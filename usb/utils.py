from user_agents import parse

from usb.models import DesktopRedirect, TabletRedirect, Mobile


def get_device_model_from_request(request):
    user_agent = parse(request.headers['User-Agent'])
    return user_agent.is_pc and DesktopRedirect or \
           user_agent.is_tablet and TabletRedirect or \
           user_agent.is_mobile and Mobile


def get_device_model_from_string(code):
    return code == DesktopRedirect.TYPE_STRING and DesktopRedirect or \
           code == TabletRedirect.TYPE_STRING and TabletRedirect or \
           code == Mobile.TYPE_STRING and Mobile
