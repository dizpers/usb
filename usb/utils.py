from user_agents import parse

from usb.models import Desktop, Tablet, Mobile


def get_device_type(request):
    user_agent = parse(request.headers['User-Agent'])
    return user_agent.is_pc and Desktop or \
           user_agent.is_tablet and Tablet or \
           user_agent.is_mobile and Mobile
