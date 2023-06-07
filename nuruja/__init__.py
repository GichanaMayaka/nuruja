from http import HTTPStatus

from flask import Flask

from .commands import create_db, drop_db, create_tables, drop_tables, recreate_tables
from .extensions import db
from .models import User
from .controllers.users import users
from .controllers.books import books
from .controllers.transactions import transactions
from ..configs import configs


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = configs.POSTGRES_DSN

    register_commands(app)
    register_extensions(app)
    register_blueprints(app)

    @app.route("/", methods=["GET"])
    def index() -> tuple[str, int]:
        return (
            "Welcome to Nuruja (https://github.com/GichanaMayaka/nuruja)",
            HTTPStatus.OK,
        )

    @app.after_request
    def set_headers(response):
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allowed-Methods"] = "GET, POST, PUT, DELETE"
        response.headers["Content-Type"] = "application/json"
        return response

    return app


def register_extensions(app: Flask) -> None:
    db.init_app(app)


def register_commands(app: Flask) -> None:
    for command in [create_db, drop_db, create_tables, drop_tables, recreate_tables]:
        app.cli.command()(command)


def register_blueprints(app: Flask) -> None:
    app.register_blueprint(users)
    app.register_blueprint(books)
    app.register_blueprint(transactions)
