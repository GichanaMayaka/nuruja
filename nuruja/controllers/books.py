from http import HTTPStatus
from typing import Union

from flask import Blueprint, jsonify
from flask.wrappers import Response
from flask_pydantic import validate
from sqlalchemy import and_

from .schemas import AllBooksSchema, BookSchema
from ..models import Book

books = Blueprint("books", __name__)


@books.route("/books", methods=["POST"])
@validate(body=BookSchema)
def add_a_book(body: BookSchema) -> tuple[Response, int]:
    book = Book.query.filter(
        and_(Book.isbn == body.isbn, Book.title == body.title, Book.author == body.author)
    ).first()

    if book:
        return jsonify(details="Book already exists"), HTTPStatus.CONFLICT

    new_book = Book.create(
        title=body.title,
        author=body.author,
        isbn=body.isbn,
        date_of_publication=body.date_of_publication,
        status=body.status,
        rent_fee=body.rent_fee,
        late_penalty_fee=body.late_penalty_fee
    )
    new_book.save()

    return jsonify(details="Book added successfully"), HTTPStatus.CREATED


@books.route("/books", methods=["GET"])
def get_all_books() -> Union[tuple[dict, int], tuple[Response, int]]:
    all_books = Book.query.all()

    if all_books:
        return AllBooksSchema(books=all_books).dict(), HTTPStatus.OK

    return jsonify(details="Book[s] not Found"), HTTPStatus.NOT_FOUND


@books.route("/books/<book_id>", methods=["GET"])
def get_single_book(book_id: int) -> Union[tuple[dict, int], tuple[Response, int]]:
    book = Book.query.filter(Book.id == book_id).first()

    if book:
        return BookSchema.from_orm(book).dict(), HTTPStatus.OK

    return jsonify(details="Book not Found"), HTTPStatus.NOT_FOUND


@books.route("/books/<book_id>", methods=["DELETE"])
def remove_book(book_id: int) -> tuple[Response, int]:
    book = Book.query.filter(Book.id == book_id).first()

    if book:
        book.delete()

        return jsonify(details="Book deleted successfully"), HTTPStatus.ACCEPTED

    return jsonify(details="Book not Found"), HTTPStatus.NOT_FOUND


@books.route("/books/<book_id>", methods=["PUT"])
@validate(body=BookSchema)
def update_book_details(book_id: int, body: BookSchema) -> tuple[Response, int]:
    book = Book.query.filter(Book.id == book_id).first()

    if book:
        book.update(
            title=body.title,
            author=body.author,
            isbn=body.isbn,
            date_of_publication=body.date_of_publication,
            status=body.status,
            rent_fee=body.rent_fee,
            late_penalty_fee=body.late_penalty_fee
        )

        return jsonify(details="Book updated successfully"), HTTPStatus.ACCEPTED

    return jsonify(details="Book not Found"), HTTPStatus.NOT_FOUND
