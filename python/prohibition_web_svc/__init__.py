from flask import Flask
from python.prohibition_web_svc.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()


def create_app(config_class=Config):
    application = Flask(__name__)
    application.config.from_object(config_class)

    db.init_app(application)
    ma.init_app(application)

    from python.prohibition_web_svc.blueprints import static, forms, admin_forms
    application.register_blueprint(admin_forms.bp)
    application.register_blueprint(static.bp)
    application.register_blueprint(forms.bp)

    from python.prohibition_web_svc.blueprints import icbc, admin_users, users
    application.register_blueprint(admin_users.bp)
    application.register_blueprint(users.bp)
    application.register_blueprint(icbc.bp)

    from python.prohibition_web_svc.blueprints import user_roles, admin_user_roles
    application.register_blueprint(admin_user_roles.bp)
    application.register_blueprint(user_roles.bp)

    # Add custom flask command line tools
    from python.prohibition_web_svc.blueprints import command_line
    application.register_blueprint(command_line.bp)

    return application
