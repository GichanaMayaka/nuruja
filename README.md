# Nuruja

This is a simple Library Management System that allows one to Add a book and member, lend a book to a member, initiate
a book return, and manage rent-fees and late penalty fees. The API is hosted on [Render](https://nuruja.onrender.com).
The front-end source code is in the [nuruja-frontend](https://github.com/GichanaMayaka/nuruja-frontend) repo

## Setup and Start (Local Setup)

Supply a _.env_ file to the root repository directory with following configurations options:

```dotenv
DEV_POSTGRES_DSN=postgresql://[user[:password]@][hostname][:port][/devDBName]
DEV_SECRET_KEY=your_development_secret_key
DEV_ALLOWED_ORIGIN=[allowed-address]

TEST_POSTGRES_DSN=postgresql://[user[:password]@][hostname][:port][/testDBName]
TEST_SECRET_KEY=your_test_secret_key
TEST_ALLOWED_ORIGIN=[allowed-address]

PROD_POSTGRES_DSN=postgresql://[user[:password]@][hostname][:port][/prodDBName]
PROD_SECRET_KEY=your_prod_secret_key
PROD_ALLOWED_ORIGIN=[allowed-address]
```

Please note that all the above configuration options are required for the application to start. Once all requisite
configuration details are supplied accordingly, quickly run the project
using [docker](https://www.docker.com/) and
[docker-compose](https://docs.docker.com/compose/):

```bash
docker-compose up -d
```

Below are all the exposed endpoints

## Books Endpoint

### Get all Books

```bash
curl -X GET http://127.0.0.1/books
```

### Get a Book by Id

```bash
curl -X GET http://127.0.0.1/books/<int:book_id>
```

### Add a Book

```bash
curl -X POST http://127.0.0.1/books \
-H 'Content-Type: application/json' \
-d '{
    "title": "Introduction to Algorithms",
    "author": "Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest, and Clifford Stein",
    "isbn": " 9780262046305",
    "date_of_publication": "1989-01-01T00:00:00",
    "status": "not-rented",
    "rent_fee": 100,
    "late_penalty_fee": 25
}'
```

### Edit/Update an Existing Book by Id

```bash
curl -X PUT http://127.0.0.1/books/<int:book_id> \
-H 'Content-Type: application/json' \
-d '{
    "title": "Introduction to Algorithms",
    "author": "Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest, and Clifford Stein",
    "isbn": " 9780262046305",
    "date_of_publication": "1989-01-01T00:00:00",
    "status": "not-rented",
    "rent_fee": 100,
    "late_penalty_fee": 25
}'
```

### Delete a Book by Id

```bash
curl -X DELETE http://127.0.0.1/books/<int:book_id>
```

## Members Endpoint

### Get all Members

```bash
curl -X GET http://127.0.0.1/members
```

### Get a Member by Id

```bash
curl -X GET http://127.0.0.1/members/<int:member_id>
```

### Add a Member

```bash
curl -X POST http://127.0.0.1/members \
-H 'Content-Type: application/json' \
-d '{
    "username": "The Crippled God",
    "email": "chained-one@gmail.com",
    "phone_number": "123654789",
    "address": "Genabackis",
    "is_admin": "false"
}'
```

### Edit/Update an Existing Member by Id

```bash
curl -X PUT http://127.0.0.1/members/<int:member_id> \
-H 'Content-Type: application/json' \
-d '{
    "username": "The Crippled God",
    "email": "chained-one@gmail.com",
    "phone_number": "123654789",
    "address": "Genabackis",
    "is_admin": "false"
}'
```

### Delete a Member by Id

```bash
curl -X DELETE http://127.0.0.1/members/<int:member_id>
```

## Borrowings Endpoint

### Initiate a Borrowing

```bash
curl -X POST http://127.0.0.1/members/<int:member_id>/borrow \
-H 'Content-Type: application/json' \
-d '{
    "book_id": 1
}'
```

### Initiate a Book Return

```bash
curl -X POST http://127.0.0.1/members/<int:member_id>/return \
-H 'Content-Type: application/json' \
-d '{
    "book_id": 1
}'
```

## Balances Enquiries

### View all Members' balances

```bash
curl -X POST 'http://127.0.0.1/balances/all'
```

### Clear a Member's balance

```bash
curl -X GET 'http://127.0.0.1/balances/<int:user_id>/all'
```

## Testing with Pytest

Run all tests with Pytest

```bash
pytest --cov --disable-warnings
```
