from . import main
from . import user
from . import auth
from . import configuration
from . import handler


def set_routes(app):
    main.set_routes(app)
    user.set_routes(app)
    auth.set_routes(app)
    configuration.set_routes(app)
    handler.set_routes(app)
