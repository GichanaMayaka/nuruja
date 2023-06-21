from http import HTTPStatus

from flask.testing import FlaskClient

from ..nuruja.models import Book


def test_add_a_book(client_app: FlaskClient, fake_available_book: Book) -> None:
    with client_app as test_client:
        response = test_client.post("/books/new",
                                    json=dict(title=fake_available_book.title, author=fake_available_book.author,
                                              date_of_publication=fake_available_book.date_of_publication,
                                              status=fake_available_book.status, isbn=fake_available_book.isbn,
                                              rent_fee=fake_available_book.rent_fee,
                                              late_penalty_fee=fake_available_book.late_penalty_fee))

    assert response.json == dict(details="Book added successfully")
    assert response.status_code == HTTPStatus.CREATED


def test_add_book_conflict(client_app: FlaskClient, fake_available_book: Book) -> None:
    with client_app as test_client:
        fake_available_book.save()
        response = test_client.post(
            "/books/new",
            json=dict(title=fake_available_book.title, author=fake_available_book.author,
                      date_of_publication='2023-06-21T13:38:51.878088+03:00',
                      status=fake_available_book.status, isbn=fake_available_book.isbn,
                      rent_fee=fake_available_book.rent_fee,
                      late_penalty_fee=fake_available_book.late_penalty_fee)
        )

    assert response.json == dict(details="Book already exists")
    assert response.status_code == HTTPStatus.CONFLICT


def test_remove_book(client_app: FlaskClient, fake_available_book: Book) -> None:
    with client_app as test_client:
        fake_available_book.save()

        response = test_client.delete(f"/books/{fake_available_book.id}/delete")

    assert response.status_code == HTTPStatus.ACCEPTED
    assert response.json == dict(details="Book deleted successfully")


def test_remove_book_failed(client_app: FlaskClient) -> None:
    with client_app as test_client:
        response = test_client.delete("/books/10000000/delete")

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json == dict(details="Book not Found")


def test_update_book(client_app: FlaskClient, fake_available_book: Book) -> None:
    with client_app as test_client:
        fake_available_book.save()

        response = test_client.put(f"/books/{fake_available_book.id}",
                                   json=dict(title="new book",
                                             author=fake_available_book.author,
                                             date_of_publication='2023-06-21T13:38:51.878088+03:00',
                                             status=fake_available_book.status,
                                             isbn=fake_available_book.isbn,
                                             rent_fee=fake_available_book.rent_fee,
                                             late_penalty_fee=fake_available_book.late_penalty_fee)
                                   )

    assert response.status_code == HTTPStatus.ACCEPTED
    assert response.json == dict(details="Book updated successfully")
    assert fake_available_book.title == "new book"


def test_update_book_failed(client_app: FlaskClient) -> None:
    with client_app as test_client:
        response = test_client.put("/books/1000000000000",
                                   json=dict(title="new book",
                                             author="author",
                                             date_of_publication='2023-06-21T13:38:51.878088+03:00',
                                             status="rented",
                                             isbn="5464564",
                                             rent_fee=10,
                                             late_penalty_fee=10)
                                   )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json == dict(details="Book not Found")


def test_get_available_books(client_app: FlaskClient, fake_available_book: Book) -> None:
    with client_app as test_client:
        fake_available_book.save()

        response = test_client.get("/books/available")

    assert isinstance(response.json["books"], list)
    assert response.status_code == HTTPStatus.OK


def test_get_available_books_failed(client_app: FlaskClient, fake_available_book: Book) -> None:
    with client_app as test_client:
        response = test_client.get("/books/available")

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json == dict(details="No Books Available")


def test_get_all_books(client_app: FlaskClient, fake_available_book: Book, fake_unavailable_book: Book) -> None:
    with client_app as test_client:
        fake_available_book.save()
        fake_unavailable_book.save()

        response = test_client.get("/books")

    assert isinstance(response.json["books"], list)
    assert len(response.json["books"]) == 2
    assert response.status_code == HTTPStatus.OK


def test_get_all_books_failed(client_app: FlaskClient) -> None:
    with client_app as test_client:
        response = test_client.get("/books")

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json == dict(details="Book[s] not Found")


def test_get_single_book(client_app: FlaskClient, fake_available_book: Book) -> None:
    with client_app as test_client:
        fake_available_book.save()

        response = test_client.get(f"/books/{fake_available_book.id}")

    assert response.status_code == HTTPStatus.OK
    assert response.json["id"] == fake_available_book.id
    assert response.json["author"] == fake_available_book.author


def test_get_single_book_failed(client_app: FlaskClient) -> None:
    with client_app as test_client:
        response = test_client.get("/books/1")

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json == dict(details="Book not Found")
