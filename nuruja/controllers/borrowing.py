from http import HTTPStatus
from typing import Final

import pendulum
from flask import Blueprint, jsonify
from flask.wrappers import Response
from flask_pydantic import validate
from sqlalchemy import and_, desc

from .schemas import BorrowBookSchema, ReturnBookSchema
from ..models import Borrowing, User, Book, UserBalance

borrowing = Blueprint("borrowing", __name__)


@borrowing.route("/users/<user_id>/borrow", methods=["POST"])
@validate(body=BorrowBookSchema)
def initiate_borrowing(user_id: int, body: BorrowBookSchema) -> tuple[Response, HTTPStatus]:
    user = User.get_by_id(user_id)
    book = Book.query.filter(
        and_(Book.id == body.book_id, Book.status != "rented")
    ).first()

    if user and book:
        new_borrow = Borrowing.create(
            user_id=user.id, book_id=book.id, rent_fee=body.rent_fee, is_return=False,
            date_borrowed=pendulum.now(),
            date_due=pendulum.now() + pendulum.duration(days=14)
        )

        previous_balance = UserBalance.query.filter(UserBalance.user_id == user.id).order_by(
            desc(UserBalance.date_of_entry)
        ).limit(1).one_or_none()

        if previous_balance:
            new_balance = UserBalance.create(
                user_id=user.id, balance=(previous_balance.balance + body.rent_fee),
                date_of_entry=pendulum.now())
            new_balance.save()

        else:
            new_balance = UserBalance.create(user_id=user.id, balance=body.rent_fee,
                                             date_of_entry=pendulum.now())
            new_balance.save()

        book.update(status="rented")
        new_borrow.save()

        return jsonify(details="Borrow Initiated"), HTTPStatus.OK

    if not user:
        return jsonify(details="The user is not registered. Please register"), HTTPStatus.NOT_FOUND

    if not book:
        return jsonify(details="The book is not available for renting"), HTTPStatus.NOT_FOUND


@borrowing.route("/users/<user_id>/return", methods=["POST"])
@validate(body=ReturnBookSchema)
def initiate_book_return(user_id: int, body: ReturnBookSchema) -> tuple[Response, HTTPStatus]:
    user = User.get_by_id(user_id)
    book = Book.query.filter(
        and_(Book.id == body.book_id, Book.status == "rented")
    ).first()
    LATE_PENALTY: Final[int] = 15

    if user and book:
        initial_borrow = Borrowing.query.filter(
            and_(Borrowing.book_id == book.id, Borrowing.user_id == user.id)
        ).first()

        previous_balance = UserBalance.query.filter(UserBalance.user_id == user.id).order_by(
            desc(UserBalance.date_of_entry)
        ).limit(1).one_or_none()

        # If late to return
        if pendulum.now().timestamp() > initial_borrow.date_due.timestamp():
            late_return = Borrowing.create(
                user_id=user.id, book_id=book.id, is_return=True, rent_fee=LATE_PENALTY,
                date_borrowed=initial_borrow.date_borrowed,
                date_due=pendulum.now()
            )

            if previous_balance:
                new_balance = UserBalance.create(
                    user_id=user.id, balance=(previous_balance.balance + LATE_PENALTY),
                    date_of_entry=pendulum.now())
                new_balance.save()

            else:
                new_balance = UserBalance.create(user_id=user.id, balance=LATE_PENALTY,
                                                 date_of_entry=pendulum.now())
                new_balance.save()

            book.update(status="not-rented")
            late_return.save()

            return jsonify(details="Late return noted. Fee of 100 applied"), HTTPStatus.OK

        # If returning on time
        new_return = Borrowing.create(user_id=user.id, book_id=book.id, is_return=True, rent_fee=0,
                                      date_borrowed=initial_borrow.date_borrowed,
                                      date_due=pendulum.now()
                                      )

        new_balance = UserBalance.create(
            user_id=user.id, balance=(previous_balance.balance - 100),
            date_of_entry=pendulum.now())
        new_balance.save()

        book.update(status="not-rented")
        new_return.save()

        return jsonify(details="Return Initiated"), HTTPStatus.OK

    if not user:
        return jsonify(details="The user is not registered. Please register"), HTTPStatus.NOT_FOUND

    if not book:
        return jsonify(details="The book has not been rented out"), HTTPStatus.NOT_FOUND
