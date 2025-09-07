from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import list_books
from .views import LibraryDetailView
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

    path("books/add/", add_book, name="add_book"),
    path("books/<int:pk>/edit/", edit_book, name="edit_book"),
    path("books/<int:pk>/delete/", delete_book, name="delete_book"),
]
