from http import HTTPStatus

import pytest
from flask import Flask
from flask.testing import FlaskClient
from sqlalchemy import create_engine
from sqlalchemy_utils import create_database, database_exists, drop_database

from configs import configs
from ..nuruja import create_app
from ..nuruja import db
from ..nuruja.controllers.schemas import MemberRequestSchema
from ..nuruja.models import User

engine = create_engine(configs.POSTGRES_DSN)


@pytest.fixture()
def create_test_database(db_engine=engine) -> None:
    if not database_exists(db_engine.url):
        create_database(db_engine.url)


@pytest.fixture()
def app(create_test_database) -> Flask:
    yield create_app()


@pytest.fixture()
def client_app(app: Flask) -> FlaskClient:
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        drop_database(engine.url)


def test_add_member(client_app: FlaskClient) -> None:
    endpoint: str = "/members/new"

    with client_app as test_client:
        response_normal_user = test_client.post(endpoint,
                                                json=MemberRequestSchema(username="tester", email="tester@email.com",
                                                                         phone_number="123456789", address="earth",
                                                                         is_admin=False).dict())

        response_admin_user = test_client.post(endpoint,
                                               json=MemberRequestSchema(username="admin", email="admin@email.com",
                                                                        phone_number="987654321", address="earth",
                                                                        is_admin=True).dict())

    assert response_normal_user.status_code == HTTPStatus.CREATED
    assert response_normal_user.json == {"details": "User added successfully"}

    assert response_admin_user.status_code == HTTPStatus.CREATED
    assert response_admin_user.json == {"details": "Admin User added successfully"}


def test_add_member_conflict(client_app: FlaskClient) -> None:
    endpoint: str = "/members/new"

    with client_app as test_client:
        conflicting_user = User.create(
            username="conflict",
            email="conflict@email.com",
            phone_number="123456789",
            address="earth",
            is_admin=False
        )
        conflicting_user.save()

        response = test_client.post(endpoint, json=MemberRequestSchema(username="conflict", email="conflict@email.com",
                                                                       phone_number="123456789", address="earth",
                                                                       is_admin=False).dict())

        assert response.status_code == HTTPStatus.CONFLICT
        assert response.json == {"details": "User already exists"}
