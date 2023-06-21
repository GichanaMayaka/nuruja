from http import HTTPStatus

from flask import Blueprint, jsonify
from flask.wrappers import Response
from flask_pydantic import validate
from sqlalchemy import and_

from .schemas import AllMembersSchema, MemberRequestSchema, MemberResponseSchema
from ..models import User

members = Blueprint("members", __name__)


@members.route("/members", methods=["GET"])
def get_all_members() -> tuple[dict, HTTPStatus] | tuple[Response, HTTPStatus]:
    all_users = User.query.all()

    if all_users:
        return AllMembersSchema(members=all_users).dict(), HTTPStatus.OK

    return jsonify(details="No Users"), HTTPStatus.NOT_FOUND


@members.route("/members/new", methods=["POST"])
@validate(body=MemberResponseSchema)
def add_member(body: MemberRequestSchema) -> tuple[Response, HTTPStatus]:
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


@members.route("/members/<int:user_id>", methods=["GET"])
def get_single_member(user_id: int) -> tuple[dict, HTTPStatus] | tuple[Response, HTTPStatus]:
    user = User.query.filter(User.id == user_id).first()

    if user:
        return MemberResponseSchema.from_orm(user).dict(), HTTPStatus.OK,

    return jsonify(details="User not found"), HTTPStatus.NOT_FOUND


@members.route("/members/<int:user_id>/delete", methods=["DELETE"])
def remove_single_member(user_id: int) -> tuple[Response, HTTPStatus]:
    user = User.query.filter(User.id == user_id).first()

    if user:
        user.delete()

        return jsonify(details="User deleted successfully"), HTTPStatus.ACCEPTED

    return jsonify(details="User not Found"), HTTPStatus.NOT_FOUND


@members.route("/members/<int:user_id>", methods=["PUT"])
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
