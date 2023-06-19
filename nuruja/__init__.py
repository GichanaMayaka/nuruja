from http import HTTPStatus

from flask import Flask

from nuruja.nuruja.commands import (create_db, create_tables, drop_db, drop_tables,
                                    recreate_tables)
from nuruja.nuruja.controllers.balances import balances
from nuruja.nuruja.controllers.books import books
from nuruja.nuruja.controllers.members import members
from nuruja.nuruja.controllers.search import search
from nuruja.nuruja.controllers.transactions import transactions
from nuruja.nuruja.extensions import db, cors, migrations
from nuruja.nuruja.models import User
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
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE"
        response.headers["Content-Type"] = "application/json"
        response.headers[
            "Access-Control-Allow-Headers"
        ] = "Origin, Content-Type, Authorization"
        return response

    return app


def register_extensions(app: Flask) -> None:
    db.init_app(app)
    cors.init_app(app)
    migrations.init_app(app, db)


def register_commands(app: Flask) -> None:
    for command in [create_db, drop_db, create_tables, drop_tables, recreate_tables]:
        app.cli.command()(command)


def register_blueprints(app: Flask) -> None:
    app.register_blueprint(members)
    app.register_blueprint(books)
    app.register_blueprint(transactions)
    app.register_blueprint(balances)
    app.register_blueprint(search)
