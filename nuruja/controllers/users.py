from http import HTTPStatus

from flask import Blueprint, jsonify
from flask.wrappers import Response
from flask_pydantic import validate
from sqlalchemy import and_

from .schemas import AllMembersSchema, MemberRequestSchema, MemberResponseSchema
from ..models import User

users = Blueprint("members", __name__)


@users.route("/members", methods=["GET"])
def get_all_members():
    all_users = User.query.all()

    if all_users:
        return AllMembersSchema(members=all_users).dict(), HTTPStatus.OK

    return jsonify(details="No Users"), HTTPStatus.NOT_FOUND


@users.route("/members/new", methods=["POST"])
@validate(body=MemberResponseSchema)
def add_member(body: MemberRequestSchema) -> tuple[Response, int]:
    existing_user: User = User.query.filter(
        and_(User.username == body.username, User.email == body.email)
    ).first()

    if existing_user:
        return jsonify(details="User already exists"), HTTPStatus.CONFLICT

    if body.is_admin:
        new_user = User.create(
            username=body.username,
            email=body.email,
            phone_number=body.phone_number,
            address=body.address,
            is_admin=body.is_admin,
        )
        new_user.save()

        return jsonify(details="Admin User added successfully"), HTTPStatus.CREATED

    new_user = User.create(
        username=body.username,
        email=body.email,
        phone_number=body.phone_number,
        address=body.address,
    )
    new_user.save()

    return jsonify(details="User added successfully"), HTTPStatus.CREATED


@users.route("/members/<user_id>", methods=["GET"])
def get_single_member(user_id: int) -> tuple[Response, int]:
    user = User.query.filter(User.id == user_id).first()

    if user:
        return (
            jsonify(
                username=user.username,
                email=user.email,
                address=user.address,
                phone_number=user.phone_number,
            ),
            HTTPStatus.OK,
        )

    return jsonify(details="User not found"), HTTPStatus.NOT_FOUND


@users.route("/members/<user_id>/delete", methods=["DELETE"])
def remove_single_member(user_id: int) -> tuple[Response, int]:
    user = User.query.filter(User.id == user_id).first()

    if user:
        user.delete()

        return jsonify(details="User deleted successfully"), HTTPStatus.ACCEPTED

    return jsonify(details="User not Found"), HTTPStatus.NOT_FOUND


@users.route("/members/<user_id>", methods=["PUT"])
@validate(body=MemberRequestSchema)
def update_single_member(
    user_id: int, body: MemberRequestSchema
) -> tuple[Response, int]:
    user_to_update = User.query.filter(User.id == user_id).first()

    if user_to_update:
        user_to_update.update(
            username=body.username,
            email=body.email,
            phone_number=body.phone_number,
            address=body.address,
            is_admin=body.is_admin,
        )

        return jsonify(details="User details updated successfully"), HTTPStatus.ACCEPTED

    return jsonify(details="User not Found"), HTTPStatus.NOT_FOUND
