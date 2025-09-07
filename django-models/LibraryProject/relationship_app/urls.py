from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import list_books, LibraryDetailView
from . import views

app_name = "relationship_app"

urlpatterns = [
    path("books/", list_books, name="list_books"),                          # FBV
    path("libraries/<int:pk>/", LibraryDetailView.as_view(),                # CBV
         name="library_detail"),

    path("login/",  LoginView.as_view(template_name="relationship_app/login.html"),   name="login"),
    path("logout/", LogoutView.as_view(template_name="relationship_app/logout.html"), name="logout"),
    path("register/", views.register, name="register"),
]
