from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView

from .models import Book, Library


# Function-based view: list all books with authors.
def list_books(request):
    books = Book.objects.select_related("author").order_by("title")

    # If you want plain-text output (meets the mandatory requirement), uncomment this block:
    """
    lines = [f"{b.title} by {b.author.name}" for b in books]
    return HttpResponse("\n".join(lines), content_type="text/plain; charset=utf-8")
    """

    # Otherwise (recommended): render an HTML template
    return render(request, "relationship_app/list_books.html", {"books": books})


# Class-based view: details for a specific library (includes its books)
class LibraryDetailView(DetailView):
    model = Library
    template_name = "relationship_app/library_detail.html"
    context_object_name = "library"
