from http import HTTPStatus
from typing import Union

from flask import Blueprint, jsonify
from flask.wrappers import Response
from flask_pydantic import validate
from sqlalchemy import and_, desc

from .schemas import (
    AllBooksSchema,
    BookRequestSchema,
    BookResponseSchema,
    UnavailableBooks,
)
from ..models import Book, Transactions, User

books = Blueprint("books", __name__)


@books.route("/books/new", methods=["POST"])
@validate(body=BookRequestSchema)
def add_a_book(body: BookRequestSchema) -> tuple[Response, int]:
    book = Book.query.filter(
        and_(
            Book.isbn == body.isbn, Book.title == body.title, Book.author == body.author
        )
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
        late_penalty_fee=body.late_penalty_fee,
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
        return BookResponseSchema.from_orm(book).dict(), HTTPStatus.OK

    return jsonify(details="Book not Found"), HTTPStatus.NOT_FOUND


@books.route("/books/<book_id>/delete", methods=["DELETE"])
def remove_book(book_id: int) -> tuple[Response, int]:
    book = Book.query.filter(Book.id == book_id).first()

    if book:
        book.delete()

        return jsonify(details="Book deleted successfully"), HTTPStatus.ACCEPTED

    return jsonify(details="Book not Found"), HTTPStatus.NOT_FOUND


@books.route("/books/<book_id>", methods=["PUT"])
@validate(body=BookRequestSchema)
def update_book_details(book_id: int, body: BookRequestSchema) -> tuple[Response, int]:
    book = Book.query.filter(Book.id == book_id).first()

    if book:
        book.update(
            title=body.title,
            author=body.author,
            isbn=body.isbn,
            date_of_publication=body.date_of_publication,
            status=body.status,
            rent_fee=body.rent_fee,
            late_penalty_fee=body.late_penalty_fee,
        )

        return jsonify(details="Book updated successfully"), HTTPStatus.ACCEPTED

    return jsonify(details="Book not Found"), HTTPStatus.NOT_FOUND


@books.route("/books/available", methods={"GET"})
def get_available_books() -> tuple[dict, HTTPStatus] | tuple[Response, HTTPStatus]:
    available_books = Book.query.filter(Book.status == "not-rented").all()

    if available_books:
        return AllBooksSchema(books=available_books).dict(), HTTPStatus.OK

    return jsonify(details="No Books Available"), HTTPStatus.NOT_FOUND


@books.route("/books/unavailable", methods=["GET"])
def get_unavailable_books() -> tuple[dict, HTTPStatus] | tuple[Response, HTTPStatus]:
    unavailable_books = (
        Transactions.query.join(User, User.id == Transactions.user_id)
        .join(Book, Book.id == Transactions.book_id)
        .filter(and_(Book.status == "rented", Transactions.is_return == False))
        .with_entities(
            User.id,
            User.username,
            Book.title,
            Book.rent_fee,
            Book.status,
            Book.late_penalty_fee,
            Book.author,
            Book.isbn,
            Transactions.date_borrowed,
            Transactions.date_due,
            Transactions.book_id,
        )
        .order_by(desc(Transactions.date_borrowed))
        .all()
    )

    if unavailable_books:
        return UnavailableBooks(books=unavailable_books).dict(), HTTPStatus.OK

    return jsonify(details="No Books Rented Out"), HTTPStatus.NOT_FOUND
