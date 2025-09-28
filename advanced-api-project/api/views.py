from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework

from .models import Book
from .serializers import BookSerializer


class BookListView(generics.ListAPIView):
    """
    GET -> List all books with filtering, searching, and ordering.

    Examples:
      Filtering: ?title=1984&publication_year=1949&author=1
      Search:    ?search=Orwell
      Ordering:  ?ordering=title or ?ordering=-publication_year
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    # Explicit backends, including the exact "filters.OrderingFilter" usage
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    # Filtering fields
    filterset_fields = ["title", "publication_year", "author"]

    # Search fields (enables text search on title and author name)
    search_fields = ["title", "author__name"]

    # Ordering fields (and default ordering)
    ordering_fields = ["title", "publication_year"]
    ordering = ["title"]


class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]


class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]


class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
