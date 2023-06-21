from http import HTTPStatus

from flask.testing import FlaskClient

from ..nuruja.controllers.schemas import BorrowBookSchema
from ..nuruja.models import User, Book


def test_initiate_borrow(client_app: FlaskClient, fake_user: User, fake_available_book: Book) -> None:
    with client_app as test_client:
        fake_user.save()
        fake_available_book.save()

        response = test_client.post(f"/members/{fake_user.id}/borrow",
                                    json=BorrowBookSchema(book_id=fake_available_book.id).dict())

    assert response.status_code == HTTPStatus.OK
    assert response.json == dict(details="Borrow Initiated")
