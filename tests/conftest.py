import pendulum
import pytest
from flask import Flask
from flask.testing import FlaskClient
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database, drop_database

from configs import configs
from ..nuruja import create_app, db
from ..nuruja.models import User, Book

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


@pytest.fixture()
def fake_user() -> User:
    user = User(
        username="tester",
        email="tester@email.com",
        address="earth",
        is_admin=False,
        phone_number="123654789"
    )
    yield user


@pytest.fixture()
def fake_admin_user() -> User:
    user = User(
        username="tester_admin",
        email="tester_admin@email.com",
        address="earth",
        is_admin=True,
        phone_number="1236547890"
    )
    yield user


@pytest.fixture()
def fake_available_book() -> Book:
    book = Book(
        title="Introduction to Algorithms",
        author="Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest, and Clifford Stein",
        isbn=9780262046305,
        date_of_publication=pendulum.now().isoformat(),
        rent_fee=100,
        late_penalty_fee=25,
        status="not-rented"
    )
    yield book


@pytest.fixture()
def fake_unavailable_book() -> Book:
    book = Book(
        title="The Mythical Man Month",
        author="Fred Brooks",
        isbn=9780201006506,
        date_of_publication=pendulum.now().isoformat(),
        rent_fee=100,
        late_penalty_fee=25,
        status="rented"
    )
    yield book
