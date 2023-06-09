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
    status: str
    rent_fee: int
    late_penalty_fee: int


class BookResponseSchema(BookRequestSchema):
    id: int


class AllBooksSchema(BaseSchema):
    books: list[BookResponseSchema]


class BorrowBookSchema(BaseSchema):
    book_id: int


class UnavailableBook(BookResponseSchema):
    username: str
    date_borrowed: DateTime
    date_due: DateTime
    book_id: int
    user_id: int


class UnavailableBooks(BaseSchema):
    books: list[UnavailableBook]


class UserBalance(BaseSchema):
    id: int
    user_id: int
    username: str
    balance: int
    date_of_entry: DateTime


class UserBalances(BaseSchema):
    balances: list[UserBalance]


class ClearUserBalancesSchema(BaseSchema):
    user_id: int


class SearchParameters(BaseSchema):
    parameters: str = ""


# The following are schemas for analytics component of the web application.
# They are tailored for compatibility with nivo charts
class PendingReturnsAnalyticsSchema(BaseSchema):
    username: str = "Total Pending Returns"
    children: list[UserBalance]


class BookStatusSchema(BaseSchema):
    id: str
    label: str
    value: int


class BookStatusAnalyticsSchema(BaseSchema):
    data: list[BookStatusSchema]


class SeriesSchema(BaseSchema):
    x: DateTime
    y: int


class BalanceSeriesAnalyticsSchema(BaseSchema):
    id: str = "Balance Amount Over Time"
    data: list[SeriesSchema]


class BalanceSeriesSchema(BaseSchema):
    data: list[BalanceSeriesAnalyticsSchema]
