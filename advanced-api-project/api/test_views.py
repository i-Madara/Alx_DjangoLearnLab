from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from .models import Author, Book

User = get_user_model()


class BookAPITests(APITestCase):
    """
    End-to-end tests for Book API:
    - CRUD endpoints
    - Permissions (read for all; write for authenticated)
    - Filtering, Searching, Ordering
    """

    @classmethod
    def setUpTestData(cls):
        # Users
        cls.user = User.objects.create_user(username="tester", password="pass12345")

        # Authors
        cls.author_orwell = Author.objects.create(name="George Orwell")
        cls.author_tolstoy = Author.objects.create(name="Leo Tolstoy")

        # Books
        cls.book_1984 = Book.objects.create(
            title="1984", publication_year=1949, author=cls.author_orwell
        )
        cls.book_animal_farm = Book.objects.create(
            title="Animal Farm", publication_year=1945, author=cls.author_orwell
        )
        cls.book_war_peace = Book.objects.create(
            title="War and Peace", publication_year=1869, author=cls.author_tolstoy
        )

        # URLs (must match api/urls.py)
        cls.url_list = reverse("book-list")  # /api/books/
        cls.url_detail_1984 = reverse("book-detail", args=[cls.book_1984.pk])
        cls.url_create = reverse("book-create")
        cls.url_update_1984 = reverse("book-update", args=[cls.book_1984.pk])
        cls.url_delete_1984 = reverse("book-delete", args=[cls.book_1984.pk])

    def setUp(self):
        self.client = APIClient()

    # ---------- READ: List & Detail (AllowAny) ----------

    def test_list_books_ok(self):
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # basic sanity: returns all 3 seeded books
        self.assertEqual(len(response.data), 3)

    def test_retrieve_book_ok(self):
        response = self.client.get(self.url_detail_1984)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "1984")

    # ---------- CREATE (IsAuthenticated) ----------

    def test_create_book_requires_auth(self):
        payload = {"title": "Homage to Catalonia", "publication_year": 1938, "author": self.author_orwell.id}
        response = self.client.post(self.url_create, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_book_ok_when_authenticated(self):
        self.client.force_authenticate(self.user)
        payload = {"title": "Homage to Catalonia", "publication_year": 1938, "author": self.author_orwell.id}
        response = self.client.post(self.url_create, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "Homage to Catalonia")
        self.assertTrue(Book.objects.filter(title="Homage to Catalonia").exists())

    # ---------- UPDATE (IsAuthenticated) ----------

    def test_update_book_requires_auth(self):
        payload = {"title": "Nineteen Eighty-Four", "publication_year": 1949, "author": self.author_orwell.id}
        response = self.client.put(self.url_update_1984, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_book_ok_when_authenticated(self):
        self.client.force_authenticate(self.user)
        payload = {"title": "Nineteen Eighty-Four", "publication_year": 1949, "author": self.author_orwell.id}
        response = self.client.put(self.url_update_1984, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Nineteen Eighty-Four")
        self.book_1984.refresh_from_db()
        self.assertEqual(self.book_1984.title, "Nineteen Eighty-Four")

    # ---------- DELETE (IsAuthenticated) ----------

    def test_delete_book_requires_auth(self):
        response = self.client.delete(self.url_delete_1984)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Book.objects.filter(pk=self.book_1984.pk).exists())

    def test_delete_book_ok_when_authenticated(self):
        self.client.force_authenticate(self.user)
        response = self.client.delete(self.url_delete_1984)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(pk=self.book_1984.pk).exists())

    # ---------- VALIDATION (publication_year not in the future) ----------

    def test_create_book_rejects_future_year(self):
        self.client.force_authenticate(self.user)
        payload = {"title": "Future Book", "publication_year": 2999, "author": self.author_orwell.id}
        response = self.client.post(self.url_create, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("publication_year", response.data)

    # ---------- FILTERING (DjangoFilterBackend) ----------

    def test_filter_by_title(self):
        response = self.client.get(self.url_list, {"title": "1984"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "1984")

    def test_filter_by_publication_year(self):
        response = self.client.get(self.url_list, {"publication_year": 1945})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [b["title"] for b in response.data]
        self.assertEqual(titles, ["Animal Farm"])

    def test_filter_by_author_id(self):
        response = self.client.get(self.url_list, {"author": self.author_orwell.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = sorted([b["title"] for b in response.data])
        self.assertEqual(titles, ["1984", "Animal Farm"])

    # ---------- SEARCH (SearchFilter) ----------

    def test_search_by_title_fragment(self):
        response = self.client.get(self.url_list, {"search": "Farm"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [b["title"] for b in response.data]
        self.assertIn("Animal Farm", titles)

    def test_search_by_author_name(self):
        response = self.client.get(self.url_list, {"search": "Tolstoy"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [b["title"] for b in response.data]
        self.assertIn("War and Peace", titles)

    # ---------- ORDERING (OrderingFilter) ----------

    def test_ordering_by_title_asc(self):
        response = self.client.get(self.url_list, {"ordering": "title"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [b["title"] for b in response.data]
        self.assertEqual(titles, ["1984", "Animal Farm", "War and Peace"])

    def test_ordering_by_publication_year_desc(self):
        response = self.client.get(self.url_list, {"ordering": "-publication_year"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [b["publication_year"] for b in response.data]
        self.assertEqual(years, sorted(years, reverse=True))
