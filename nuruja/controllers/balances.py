from http import HTTPStatus

from flask import Blueprint, Response, jsonify
from sqlalchemy import text

from ..extensions import db
from .schemas import UserBalances

balances = Blueprint("balances", __name__)


@balances.route("/balances/all", methods=["GET"])
def get_all_user_balances() -> tuple[dict, HTTPStatus] | tuple[Response, HTTPStatus]:
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
        return UserBalances(balances=user_balances).dict(), HTTPStatus.OK

    return jsonify(details="Not Found."), HTTPStatus.NOT_FOUND
