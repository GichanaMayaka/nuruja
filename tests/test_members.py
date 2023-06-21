from http import HTTPStatus

from flask.testing import FlaskClient

from ..nuruja.controllers.schemas import MemberRequestSchema
from ..nuruja.models import User


def test_add_member(client_app: FlaskClient, fake_user: User, fake_admin_user: User) -> None:
    endpoint: str = "/members/new"

    with client_app as test_client:
        response_normal_user = test_client.post(endpoint,
                                                json=MemberRequestSchema.from_orm(fake_user).dict())

        response_admin_user = test_client.post(endpoint,
                                               json=MemberRequestSchema.from_orm(fake_admin_user).dict())

    assert response_normal_user.json == {"details": "User added successfully"}
    assert response_normal_user.status_code == HTTPStatus.CREATED

    assert response_admin_user.json == {"details": "Admin User added successfully"}
    assert response_admin_user.status_code == HTTPStatus.CREATED


def test_add_member_conflict(client_app: FlaskClient, fake_user: User) -> None:
    endpoint: str = "/members/new"

    with client_app as test_client:
        fake_user.save()

        response = test_client.post(endpoint, json=MemberRequestSchema.from_orm(fake_user).dict())

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json == {"details": "User already exists"}


def test_delete_member(client_app: FlaskClient, fake_user: User) -> None:
    with client_app as test_client:
        fake_user.save()

        response = test_client.delete(f"/members/{fake_user.id}/delete")

    assert response.status_code == HTTPStatus.ACCEPTED
    assert response.json == dict(details="User deleted successfully")


def test_delete_member_failed(client_app: FlaskClient) -> None:
    with client_app as test_client:
        response = test_client.delete("/members/10000000000/delete")

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json == dict(details="User not Found")


def test_update_member(client_app: FlaskClient, fake_user: User) -> None:
    with client_app as test_client:
        fake_user.save()

        response = test_client.put(f"/members/{fake_user.id}",
                                   json=MemberRequestSchema(username="deleter", email="deleter@email.com",
                                                            phone_number="321654987", address="world").dict())

    assert response.status_code == HTTPStatus.ACCEPTED
    assert response.json == dict(details="User details updated successfully")
    assert fake_user.username == "deleter"


def test_update_member_failed(client_app: FlaskClient, fake_user: User) -> None:
    with client_app as test_client:
        response = test_client.put("/members/1000000",
                                   json=MemberRequestSchema.from_orm(fake_user).dict())

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json == dict(details="User not Found")


def test_get_all_members(client_app: FlaskClient, fake_user: User, fake_admin_user: User) -> None:
    with client_app as test_client:
        fake_user.save()
        fake_admin_user.save()

        response = test_client.get("/members")

    assert isinstance(response.json["members"], list)
    assert len(response.json["members"]) == 2
    assert response.status_code == HTTPStatus.OK


def test_get_all_members_failed(client_app: FlaskClient) -> None:
    with client_app as test_client:
        response = test_client.get("/members")

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json == dict(details="No Users")
