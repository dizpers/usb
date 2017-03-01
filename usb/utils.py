from user_agents import parse

from usb.models import DeviceType


def get_device_type(request):
    user_agent = parse(request.headers['User-Agent'])
    return user_agent.is_pc and DeviceType.DESKTOP or \
           user_agent.is_tablet and DeviceType.TABLET or \
           user_agent.is_mobile and DeviceType.MOBILE
