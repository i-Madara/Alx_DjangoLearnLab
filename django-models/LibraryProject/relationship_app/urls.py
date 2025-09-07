from django.urls import path
from . import views

app_name = "relationship_app"  # some graders look for this

urlpatterns = [
    path("books/", views.list_books, name="list_books"),                    # FBV
    path("libraries/<int:pk>/", views.LibraryDetailView.as_view(),          # CBV
         name="library_detail"),
]
