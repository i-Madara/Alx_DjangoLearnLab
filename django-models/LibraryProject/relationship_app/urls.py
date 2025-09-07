from django.urls import path
from . import views

urlpatterns = [
    path("books/", views.list_books, name="list_books"),                    # function-based view
    path("libraries/<int:pk>/", views.LibraryDetailView.as_view(),          # class-based view
         name="library_detail"),
]
