
from app.resources import user_content


def set_routes(app):

    app.add_url_rule("/user/<int:user_id>/assignment",
                     "user_content_index", user_content.index)
    app.add_url_rule("/user/<int:user_id>/assign/<int:element_id>",
                     "user_content_assign", user_content.assign)
    app.add_url_rule("/user/<int:user_id>/unassign/<int:element_id>",
                     "user_content_unassign", user_content.unassign)
