
from app.resources import employee_review


def set_routes(app):

    app.add_url_rule("/employee_review",
                     "employee_review_index", employee_review.index)
    app.add_url_rule("/employee_review/see/<int:review_id>",
                     "employee_review_see", employee_review.see)
