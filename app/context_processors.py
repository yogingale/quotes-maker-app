from flask import request


"""
Jinja2 context processors


"""


def is_active_link(link_names):
    """
    check the passed in collection of link names with the current
    url.  If there is a match, return 'active', else empty string

    Typical usage:
    <li class="{{ is_active_link( [url_for('user.user_profile')] ) }}">


    :param link_names: collection of link names.
    :return: string 'active' is the current url matches the parameter, else empty string.
    """
    current_url_rule = request.url_rule.rule
    if current_url_rule in link_names:
        return "active"
    else:
        return ""
