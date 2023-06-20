from http import HTTPStatus

import pendulum
from flask import Blueprint, Response, jsonify
from flask_pydantic import validate
from sqlalchemy import text

from .schemas import UserBalances, ClearUserBalancesSchema
from ..extensions import db
from ..models import User, UserBalance

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


@balances.route("/balances/clear", methods=["POST"])
@validate(body=ClearUserBalancesSchema)
def clear_user_balances(body: ClearUserBalancesSchema) -> tuple[Response, HTTPStatus]:
    user = User.get_by_id(body.user_id)

    if user:
        user_balance = UserBalance.create(
            balance=0,
            date_of_entry=pendulum.now(),
            user_id=user.id
        )

        user_balance.save()
        return jsonify(details="Balance Cleared"), HTTPStatus.ACCEPTED

    return jsonify(details="User not Found"), HTTPStatus.NOT_FOUND
