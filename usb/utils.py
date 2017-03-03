from user_agents import parse

from usb.models import DesktopRedirect, TabletRedirect, MobileRedirect


def get_device_model_from_request(request):
    """
    Get a specific redirect model class by analyzing given request
    :param request: Request to be analyzed
    :return: Device-specific redirect model class
    :rtype: DesktopRedirect or TabletRedirect or MobileRedirect
    """
    user_agent = parse(request.headers['User-Agent'])
    return user_agent.is_pc and DesktopRedirect or \
           user_agent.is_tablet and TabletRedirect or \
           user_agent.is_mobile and MobileRedirect


def get_device_model_from_string(code):
    """
    Get a specific redirect model class by string type code
    :param code: String type code
    :return: Device-specific redirect model class
    :rtype: DesktopRedirect or TabletRedirect or MobileRedirect
    """
    return code == DesktopRedirect.TYPE_STRING and DesktopRedirect or \
           code == TabletRedirect.TYPE_STRING and TabletRedirect or \
           code == MobileRedirect.TYPE_STRING and MobileRedirect
