from typing import Optional

from pendulum import DateTime
from pydantic import BaseModel


class BaseSchema(BaseModel):
    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class MemberRequestSchema(BaseSchema):
    username: str
    email: str
    phone_number: str
    address: str
    is_admin: Optional[bool] = False


class MemberResponseSchema(MemberRequestSchema):
    id: int


class AllMembersSchema(BaseSchema):
    members: Optional[list[MemberResponseSchema]]


class BookRequestSchema(BaseSchema):
    title: str
    author: str
    isbn: str
    date_of_publication: DateTime
    category: Optional[str]
    status: str
    rent_fee: int
    late_penalty_fee: int


class BookResponseSchema(BookRequestSchema):
    id: int


class AllBooksSchema(BaseSchema):
    books: list[BookResponseSchema]


class BorrowBookSchema(BaseSchema):
    book_id: int
