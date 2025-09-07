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

# -> Project root = folder that contains manage.py
BASE_DIR = pathlib.Path(__file__).resolve().parents[1]  # …/LibraryProject/
sys.path.insert(0, str(BASE_DIR))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "LibraryProject.settings")

import django  # noqa: E402
django.setup()

from relationship_app.models import Author, Library  # noqa: E402


def books_by_author(author_name: str) -> None:
    author = Author.objects.filter(name__iexact=author_name).first()
    if not author:
        print(f"No author found with name '{author_name}'.")
        return

    qs = author.books.all().order_by("title")
    print(f"Books by {author.name} ({qs.count()}):")
    for b in qs:
        print(f"- {b.title}")


def books_in_library(library_name: str) -> None:
    library = Library.objects.filter(name__iexact=library_name).first()
    if not library:
        print(f"No library found named '{library_name}'.")
        return

    qs = library.books.select_related("author").order_by("title")
    print(f"Books in {library.name} ({qs.count()}):")
    for b in qs:
        print(f"- {b.title} — {b.author.name}")


def librarian_for_library(library_name: str) -> None:
    library = Library.objects.filter(name__iexact=library_name).select_related("librarian").first()
    if not library:
        print(f"No library found named '{library_name}'.")
        return

    if hasattr(library, "librarian"):
        print(f"Librarian for {library.name}: {library.librarian.name}")
    else:
        print(f"{library.name} has no librarian assigned yet.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run sample ORM relationship queries.")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p1 = sub.add_parser("books-by-author", help="List all books by an author (case-insensitive).")
    p1.add_argument("author", help="Author name")

    p2 = sub.add_parser("books-in-library", help="List all books in a library (case-insensitive).")
    p2.add_argument("library", help="Library name")

    p3 = sub.add_parser("librarian-for-library", help="Show the librarian assigned to a library.")
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
