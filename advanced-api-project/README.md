API Endpoints:
- GET /api/books/ → list all books
- POST /api/books/ → create a new book (auth required)
- GET /api/books/<id>/ → retrieve book by ID
- PUT /api/books/<id>/ → update book (auth required)
- DELETE /api/books/<id>/ → delete book (auth required)

Filtering:
- GET /api/books/?title=1984
- GET /api/books/?author=1
- GET /api/books/?publication_year=1949

Searching:
- GET /api/books/?search=Orwell
- GET /api/books/?search=Farm

Ordering:
- GET /api/books/?ordering=title
- GET /api/books/?ordering=-publication_year