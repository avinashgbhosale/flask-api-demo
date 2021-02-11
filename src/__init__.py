# - coding: utf-8 --
from flask_restx import Api

from src.custom_exceptions import ValidationError, NotFoundError, NotAuthorizedError, ServerError
from src.extensions import app

from src.apis.files import ns as files_ns
from src.apis.orders import api as orders_ns
from src.apis.github import api as github_ns

api = Api(app, version='1.0', title='DEMO API', description='Flask Demo API')
api.add_namespace(files_ns, "/files")
api.add_namespace(orders_ns, "/orders")
api.add_namespace(github_ns, "/github")

# @login_manager.user_loader
# def load_user(user_id):
#     return User.get(user_id)


# def register_extensions(app):
#     with app.app_context():
#         db.init_app(app)


# def configure_database(app):
#     @app.before_first_request
#     def initialize_database():
#         db.create_all(app=app)
#         # update_db()
#
#     @app.teardown_appcontext
#     def shutdown_session(response_or_exc):
#         db.session.remove()


# def register_blueprints(app):
#     app.register_blueprint(api_blueprint)
#     app.register_blueprint(view_blueprint)


'''
def configure_logs(app):
    logger = logging.getLogger()
    logger.setLevel(logging.ERROR)
    handler = TimedRotatingFileHandler('error.log', when='midnight', interval=1, backupCount=12)
    handler.suffix = "%Y_%m_%d" + ".log"
    logger.addHandler(handler)
'''


@api.errorhandler(NotFoundError)
@api.errorhandler(NotAuthorizedError)
@api.errorhandler(ValidationError)
def handle_error(error):
    return error.to_dict(), getattr(error, 'code')


# @api.errorhandler(Exception)
# def default_error_handler(error):
#     """Returns Internal server error"""
#     error = ServerError()
#     return error.to_dict(), getattr(error, 'code', 500)


def create_app(config):
    app.config.from_object(config)
    # register_extensions(app)
    # register_blueprints(app)
    # configure_database(app)
    # configure_logs(app)
    return app
