from http import HTTPStatus

import pendulum
from flask.testing import FlaskClient
from sqlalchemy import and_

from ..nuruja.controllers.schemas import BorrowBookSchema
from ..nuruja.models import User, Book, Transactions, UserBalance


def test_initiate_borrow(client_app: FlaskClient, fake_user: User, fake_available_book: Book) -> None:
    with client_app as test_client:
        fake_user.save()
        fake_available_book.save()

        response = test_client.post(f"/members/{fake_user.id}/borrow",
                                    json=BorrowBookSchema(book_id=fake_available_book.id).dict())

    assert response.status_code == HTTPStatus.OK
    assert response.json == dict(details="Borrow Initiated")
    assert fake_available_book.status == "rented"


def test_initiate_return(client_app: FlaskClient, fake_user: User, fake_unavailable_book: Book) -> None:
    date_borrowed: pendulum.DateTime = pendulum.now()
    date_due: pendulum.datetime = date_borrowed + pendulum.duration(days=1)

    with client_app as test_client:
        fake_user.save()
        fake_unavailable_book.save()

        transaction = Transactions.create(is_return=False, rent_fee=100, date_borrowed=date_borrowed, date_due=date_due,
                                          user_id=fake_user.id,
                                          book_id=fake_unavailable_book.id)

        UserBalance.create(balance=transaction.rent_fee, date_of_entry=transaction.date_borrowed,
                           user_id=fake_user.id, transaction_id=transaction.id)

        response = test_client.post(f"/members/{fake_user.id}/return",
                                    json=BorrowBookSchema(book_id=fake_unavailable_book.id).dict())

    balance: int = UserBalance.query.filter(
        and_(UserBalance.user_id == fake_user.id, UserBalance.transaction_id == transaction.id)).first().balance

    assert response.json == dict(details="Return Initiated")
    assert response.status_code == HTTPStatus.OK
    assert balance == fake_unavailable_book.rent_fee
    assert fake_unavailable_book.status == "not-rented"


def test_initiate_late_return(client_app: FlaskClient, fake_user: User, fake_unavailable_book: Book) -> None:
    date_borrowed: pendulum.DateTime = pendulum.now()
    date_due: pendulum.datetime = date_borrowed + pendulum.duration(days=30)

    with client_app as test_client:
        fake_user.save()
        fake_unavailable_book.save()

        transaction = Transactions.create(is_return=False, rent_fee=100, date_borrowed=date_borrowed, date_due=date_due,
                                          user_id=fake_user.id,
                                          book_id=fake_unavailable_book.id)

        UserBalance.create(balance=transaction.rent_fee, date_of_entry=transaction.date_borrowed,
                           user_id=fake_user.id, transaction_id=transaction.id)

        response = test_client.post(f"/members/{fake_user.id}/return",
                                    json=BorrowBookSchema(book_id=fake_unavailable_book.id).dict())

    balance: int = (UserBalance.query.filter(
        and_(UserBalance.user_id == fake_user.id,
             UserBalance.transaction_id == transaction.id)).first().balance + fake_unavailable_book.late_penalty_fee)

    assert response.json == dict(details="Return Initiated")
    assert response.status_code == HTTPStatus.OK
    assert balance == (fake_unavailable_book.rent_fee + fake_unavailable_book.late_penalty_fee)
    assert fake_unavailable_book.status == "not-rented"
