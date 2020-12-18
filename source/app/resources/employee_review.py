
from flask import render_template, url_for, request, redirect

from app.models import Configuration, EmployeeReview
from app.models.alert import Alert
from app.helpers.alert import add_alert, get_alert
from app.helpers.permission import permission
from app.helpers.forms import EmployeeForm


@permission('employee_review_index')
def index():

    page = int(request.args.get('page', 1))
    per_page = Configuration.get().items_per_page
    reviews = EmployeeReview.all_paginated(page, per_page)

    return render_template("employee/review_index.html", reviews=reviews, alert=get_alert())


@permission('employee_review_see')
def see(review_id):
    employee_review = EmployeeReview.get(review_id)
    if not employee_review:
        add_alert(Alert("danger", "No existe la revisión especificada."))
        return redirect(url_for("employee_review_index"))

    employee_review.see()

    return redirect(url_for("employee_review_index", **request.args))
