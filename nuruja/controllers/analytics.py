from http import HTTPStatus

from flask import Blueprint, jsonify
from flask.wrappers import Response
from sqlalchemy import func, text

from ..extensions import db
from ..models import Book, UserBalance
from .schemas import (BalanceSeriesAnalyticsSchema, BookStatusAnalyticsSchema,
                      PendingReturnsAnalyticsSchema)

analytics = Blueprint("analytics", __name__, url_prefix="/analytics")


@analytics.route("/pending-returns", methods=["GET"])
def get_pending_returns() -> tuple[dict, HTTPStatus] | tuple[Response, HTTPStatus]:
    sql = text(
        """
            WITH cte AS (
                SELECT *, ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY date_of_entry DESC) row_nums
                    FROM user_balance
            )
            SELECT c.id, c.user_id, u.username, c.balance, c.date_of_entry 
                FROM cte c INNER JOIN public.user u ON c.user_id = u.id
                    WHERE c.row_nums = 1
        """
    )

    user_balances = db.session.execute(sql).fetchall()

    if user_balances:
        return PendingReturnsAnalyticsSchema(children=user_balances).dict(), HTTPStatus.OK

    return jsonify(details="Not Found."), HTTPStatus.NOT_FOUND


@analytics.route("/book-status", methods=["GET"])
def get_book_statuses() -> tuple[dict, HTTPStatus] | tuple[Response, HTTPStatus]:
    books = Book.query.with_entities(Book.status.label("id"), Book.status.label("label"),
                                     func.count(Book.status).label("value")).group_by(
        Book.status).all()

    if books:
        return BookStatusAnalyticsSchema(data=books).dict(), HTTPStatus.OK

    return jsonify(details="Not Found."), HTTPStatus.NOT_FOUND


@analytics.route("/balances-series", methods=["GET"])
def get_balance_time_series() -> tuple[Response, HTTPStatus] | tuple[dict, HTTPStatus]:
    series = UserBalance.query.with_entities(func.date_trunc("day", UserBalance.date_of_entry).label("x"),
                                             func.sum(UserBalance.balance).label("y")).group_by(
        func.date_trunc('day', UserBalance.date_of_entry)).all()

    if series:
        return BalanceSeriesAnalyticsSchema(id="Balances Over Time", data=series).dict(), HTTPStatus.OK

    return jsonify(details="Not Found."), HTTPStatus.NOT_FOUND
