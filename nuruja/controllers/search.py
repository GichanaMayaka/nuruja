from http import HTTPStatus

from flask import Blueprint, jsonify, Response
from flask_pydantic import validate
from sqlalchemy import or_

from .schemas import SearchParameters, AllBooksSchema
from ..models import Book

search = Blueprint("search", __name__)


@search.route("/filter", methods=["POST"])
@validate(body=SearchParameters)
def search_for_book(body: SearchParameters) -> tuple[dict, HTTPStatus] | tuple[Response, HTTPStatus]:
    books_search_results = Book.query.filter(
        or_(Book.title.ilike(f'%{body.parameters}%'), Book.author.ilike(f"%{body.parameters}%"))).all()

    if books_search_results:
        return AllBooksSchema(books=books_search_results).dict(), HTTPStatus.OK

    return jsonify(details="Not Found"), HTTPStatus.NOT_FOUND
