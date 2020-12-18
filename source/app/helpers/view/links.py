
from flask import url_for

from app.helpers.permission import verify_permission


def link(object_, attribute, endpoint):
    object_property = getattr(object_, attribute)

    if not callable(object_property):
        visible_content = object_property
    else:
        visible_content = object_property()

    if verify_permission(permission=endpoint, id=object_.id):
        html_format = '<a href="{}" style="text-decoration: none;">{{}}</a>'.format(
            url_for(endpoint, id=object_.id)
        )
    else:
        html_format = "{}"

    return html_format.format(visible_content)
