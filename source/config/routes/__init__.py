
from . import main
from . import auth
from . import configuration
from . import handler
from . import user
from . import user_content
from . import role
from . import permission
from . import career
from . import cathedra
from . import office
from . import charge
from . import employee
from . import pending_employee
from . import employee_review
from . import job_position
from . import request
from . import request_type


def set_routes(app):

    main.set_routes(app)
    auth.set_routes(app)
    configuration.set_routes(app)
    handler.set_routes(app)
    user.set_routes(app)
    user_content.set_routes(app)
    role.set_routes(app)
    permission.set_routes(app)
    career.set_routes(app)
    cathedra.set_routes(app)
    office.set_routes(app)
    charge.set_routes(app)
    employee.set_routes(app)
    pending_employee.set_routes(app)
    employee_review.set_routes(app)
    job_position.set_routes(app)
    request.set_routes(app)
    request_type.set_routes(app)
