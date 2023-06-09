from http import HTTPStatus

import pendulum
import pytz
from flask import Blueprint, jsonify
from flask.wrappers import Response
from flask_pydantic import validate
from sqlalchemy import and_, desc

from .schemas import BorrowBookSchema
from ..models import Book, Transactions, User, UserBalance

transactions = Blueprint("transactions", __name__)


@transactions.route("/members/<int:user_id>/borrow", methods=["POST"])
@validate(body=BorrowBookSchema)
def initiate_borrow(
        user_id: int, body: BorrowBookSchema
) -> tuple[Response, HTTPStatus]:
    user = User.get_by_id(user_id)
    book = Book.query.filter(
        and_(Book.id == body.book_id, Book.status != "rented")
    ).first()

    if user and book:
        new_borrow = Transactions.create(
            user_id=user.id,
            book_id=book.id,
            rent_fee=book.rent_fee,
            is_return=False,
            date_borrowed=pendulum.now(),
            date_due=pendulum.now() + pendulum.duration(days=14),
        )

        previous_balance = (
            UserBalance.query.filter(UserBalance.user_id == user.id)
            .order_by(desc(UserBalance.date_of_entry))
            .first()
        )

        if previous_balance:
            new_amount = (previous_balance.balance + book.rent_fee)

            if new_amount <= 500:
                new_balance = UserBalance.create(
                    user_id=user.id,
                    balance=new_amount,
                    date_of_entry=pendulum.now(),
                    transaction_id=new_borrow.id,
                )
                new_balance.save()

            else:
                return jsonify(
                    details="Balance is/will be above cut-off. Cannot rent to member"), HTTPStatus.NOT_ACCEPTABLE

        else:
            new_balance = UserBalance.create(
                user_id=user.id,
                balance=book.rent_fee,
                date_of_entry=pendulum.now(),
                transaction_id=new_borrow.id,
            )
            new_balance.save()

        book.update(status="rented")
        new_borrow.save()

        return jsonify(details="Borrow Initiated"), HTTPStatus.OK

    if not user:
        return (
            jsonify(details="The user is not registered. Please register"),
            HTTPStatus.NOT_FOUND,
        )

    if not book:
        return (
            jsonify(details="The book is not available for renting"),
            HTTPStatus.NOT_FOUND,
        )


@transactions.route("/members/<int:user_id>/return", methods=["POST"])
@validate(body=BorrowBookSchema)
def initiate_book_return(
        user_id: int, body: BorrowBookSchema
) -> tuple[Response, HTTPStatus]:
    user = User.get_by_id(user_id)
    book = Book.query.filter(
        and_(Book.id == body.book_id, Book.status == "rented")
    ).first()
    utc = pytz.UTC

    if user and book:
        initial_borrow = Transactions.query.filter(
            and_(Transactions.book_id == book.id, Transactions.user_id == user.id, Transactions.is_return == False)
        ).order_by(desc(Transactions.date_borrowed)).first()

        previous_balance = (
            UserBalance.query.filter(UserBalance.user_id == user.id)
            .order_by(desc(UserBalance.date_of_entry))
            .first()
        )

        # If late to return
        if pendulum.now().replace(tzinfo=utc) > initial_borrow.date_due.replace(tzinfo=utc):
            late_return = Transactions.create(
                user_id=user.id,
                book_id=book.id,
                is_return=True,
                rent_fee=book.late_penalty_fee,
                date_borrowed=initial_borrow.date_borrowed,
                date_due=pendulum.now(),
            )

            new_balance = UserBalance.create(
                user_id=user.id,
                balance=((previous_balance.balance - book.rent_fee) + book.late_penalty_fee),
                date_of_entry=pendulum.now(),
                transaction_id=late_return.id,
            )

            book.update(status="not-rented")
            new_balance.save()
            late_return.save()

            return (
                jsonify(details=f"Late return noted. Fee of {book.late_penalty_fee} applied"), HTTPStatus.OK,
            )

        # If returning on time
        new_return = Transactions.create(
            user_id=user.id,
            book_id=book.id,
            is_return=True,
            rent_fee=0,
            date_borrowed=initial_borrow.date_borrowed,
            date_due=pendulum.now(),
        )

        new_balance = UserBalance.create(
            user_id=user.id,
            balance=(previous_balance.balance - book.rent_fee),
            date_of_entry=pendulum.now(),
            transaction_id=new_return.id,
        )
        new_balance.save()

        book.update(status="not-rented")
        new_return.save()

        return jsonify(details="Return Initiated"), HTTPStatus.OK

    if not user:
        return (
            jsonify(details="The user is not registered. Please register"),
            HTTPStatus.NOT_FOUND,
        )

    if not book:
        return jsonify(details="The book has not been rented out"), HTTPStatus.NOT_FOUND
