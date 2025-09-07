from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from .views import list_books, LibraryDetailView
from .views import add_book, edit_book, delete_book
from . import views

app_name = "relationship_app"

urlpatterns = [
    path("", list_books, name="home"),

    path("books/", list_books, name="list_books"),
    path("libraries/<int:pk>/", LibraryDetailView.as_view(), name="library_detail"),

    path("login/",  LoginView.as_view(template_name="relationship_app/login.html"),   name="login"),
    path("logout/", LogoutView.as_view(template_name="relationship_app/logout.html"), name="logout"),
    path("register/", views.register, name="register"),

    path("roles/admin/", views.admin_view, name="admin_view"),
    path("roles/librarian/", views.librarian_view, name="librarian_view"),
    path("roles/member/", views.member_view, name="member_view"),

    path("add_book/", add_book, name="add_book"),
    path("edit_book/<int:pk>/", edit_book, name="edit_book"),
    path("delete_book/<int:pk>/", delete_book, name="delete_book"),
]
