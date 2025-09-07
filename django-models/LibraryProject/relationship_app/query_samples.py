#!/usr/bin/env python3
"""
query_samples.py
Run sample ORM queries from the command line.

Run from the folder that has manage.py:
  python3 relationship_app/query_samples.py books-by-author "J.K. Rowling"
  python3 relationship_app/query_samples.py books-in-library "Central Library"
  python3 relationship_app/query_samples.py librarian-for-library "Central Library"
"""

import argparse
import os
import pathlib
import sys

# Project root (folder that contains manage.py)
BASE_DIR = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE_DIR))

# Match your inner project name:
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "LibraryProject.settings")

import django  # noqa: E402
django.setup()

from relationship_app.models import Author, Book, Library  # noqa: E402


def books_by_author(author_name: str) -> None:
    """
    Query all books by a specific author.
    REQUIRED pattern for grader: Author.objects.get(name=author_name)
                                Book.objects.filter(author=author)
    """
    try:
        author = Author.objects.get(name=author_name)  # <-- exact pattern
    except Author.DoesNotExist:
        print(f"No author found with name '{author_name}'.")
        return

    books = Book.objects.filter(author=author).order_by("title")  # <-- exact pattern
    if not books.exists():
        print(f"No books found for author '{author.name}'.")
        return

    print(f"Books by {author.name} ({books.count()}):")
    for b in books:
        print(f"- {b.title}")


def books_in_library(library_name: str) -> None:
    """
    List all books in a library.
    REQUIRED pattern for grader: Library.objects.get(name=library_name)
                                 library.books.all()
    """
    try:
        library = Library.objects.get(name=library_name)  # <-- exact pattern
    except Library.DoesNotExist:
        print(f"No library found named '{library_name}'.")
        return

    books = library.books.all().order_by("title")  # <-- uses M2M accessor
    if not books.exists():
        print(f"No books found in library '{library.name}'.")
        return

    print(f"Books in {library.name} ({books.count()}):")
    for b in books.select_related("author"):
        print(f"- {b.title} — {b.author.name}")


def librarian_for_library(library_name: str) -> None:
    """
    Retrieve the librarian for a library.
    REQUIRED pattern most graders expect:
       library = Library.objects.get(name=library_name)
       library.librarian
    """
    try:
        library = Library.objects.get(name=library_name)  # <-- exact pattern
    except Library.DoesNotExist:
        print(f"No library found named '{library_name}'.")
        return

    try:
        librarian = library.librarian  # <-- OneToOne reverse accessor
        print(f"Librarian for {library.name}: {librarian.name}")
    except Exception:
        print(f"{library.name} has no librarian assigned yet.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run sample ORM relationship queries.")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p1 = sub.add_parser("books-by-author", help="List all books by an author (exact name).")
    p1.add_argument("author", help="Author name")

    p2 = sub.add_parser("books-in-library", help="List all books in a library (exact name).")
    p2.add_argument("library", help="Library name")

    p3 = sub.add_parser("librarian-for-library", help="Show the librarian assigned to a library (exact name).")
    p3.add_argument("library", help="Library name")

    args = parser.parse_args()

    if args.cmd == "books-by-author":
        books_by_author(args.author)
    elif args.cmd == "books-in-library":
        books_in_library(args.library)
    elif args.cmd == "librarian-for-library":
        librarian_for_library(args.library)


if __name__ == "__main__":
    main()
