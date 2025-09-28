from rest_framework import generics, permissions
from .models import Book
from .serializers import BookSerializer


# List all books or create a new one
class BookListCreateView(generics.ListCreateAPIView):
    """
    GET -> List all books
    POST -> Create a new book (authenticated users only)
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    # Permissions: allow anyone to read, only authenticated can create
    def get_permissions(self):
        if self.request.method == "POST":
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]


# Retrieve, update, or delete a book
class BookRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET -> Retrieve a book by ID
    PUT/PATCH -> Update book (authenticated users only)
    DELETE -> Delete book (authenticated users only)
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_permissions(self):
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]
