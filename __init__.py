from flask import Flask
from flask_bootstrap import Bootstrap
import pymongo as pymongo

bootstrap = Bootstrap()


def create_app():
    app = Flask(__name__)
    bootstrap.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .corporation import corporation as corporation_blueprint
    app.register_blueprint(corporation_blueprint, url_prefix='/corporation')

    from .report import report as report_blueprint
    app.register_blueprint(report_blueprint, url_prefix='/report')

    from .sector import sector as sector_blueprint
    app.register_blueprint(sector_blueprint, url_prefix='/sector')

    return app