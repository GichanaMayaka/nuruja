from http import HTTPStatus

from flask import Flask

from .commands import create_db, drop_db, create_tables, drop_tables, recreate_tables
from .extensions import db
from .models import User
from ..configs import configs


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = configs.POSTGRES_DSN

    register_commands(app)
    register_extensions(app)
    register_blueprints(app)

    @app.route("/", methods=["GET"])
    def index() -> tuple[str, int]:
        return "Welcome to Nuruja (https://github.com/GichanaMayaka/nuruja)", HTTPStatus.OK

    return app


def register_extensions(app: Flask) -> None:
    db.init_app(app)


def register_commands(app: Flask) -> None:
    for command in [create_db, drop_db, create_tables, drop_tables, recreate_tables]:
        app.cli.command()(command)


def register_blueprints(app: Flask) -> None:
    return
