from http import HTTPStatus

from flask import Flask
from .commands import create_db, drop_db
from ..configs import configs


def create_app() -> Flask:
    app = Flask(__name__)

    register_commands(app)
    register_extensions(app)
    register_blueprints(app)

    @app.route("/", methods=["GET"])
    def index() -> tuple[str, int]:
        return "Welcome to Nuruja (https://github.com/GichanaMayaka/nuruja)", HTTPStatus.OK

    return app


def register_extensions(app: Flask) -> None:
    return


def register_commands(app: Flask) -> None:
    for command in [create_db, drop_db]:
        app.cli.command()(command)


def register_blueprints(app: Flask) -> None:
    return
