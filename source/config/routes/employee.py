
from app.resources import employee

def set_routes(app):

    app.add_url_rule("/employees", "employee_index", employee.index)
    app.add_url_rule("/employee/show/<int:id>", "employee_show", employee.show)
    app.add_url_rule("/employee/new", "employee_new", employee.new)
    app.add_url_rule("/employee/create", "employee_create", employee.create, methods=["POST"])
    app.add_url_rule("/employee/edit/<int:id>", "employee_edit", employee.edit)
    app.add_url_rule("/employee/update/<int:id>", "employee_update", employee.update, methods=["POST"])
    app.add_url_rule("/employee/delete/<int:id>", "employee_delete", employee.delete)
