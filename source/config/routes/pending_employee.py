
from app.resources import pending_employee

def set_routes(app):

    app.add_url_rule("/pending_employees", "pending_employee_index", pending_employee.index)
    app.add_url_rule("/pending_employee/show/<int:id>", "pending_employee_show", pending_employee.show)
    app.add_url_rule("/pending_employee/accept/<int:id>", "pending_employee_accept", pending_employee.accept)
    app.add_url_rule("/pending_employee/reject/<int:id>", "pending_employee_reject", pending_employee.reject)
