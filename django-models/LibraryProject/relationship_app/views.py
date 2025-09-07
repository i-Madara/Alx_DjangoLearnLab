from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login
from django.views.generic.detail import DetailView  
from .models import Book
from .models import Library
from django.contrib.auth.decorators import user_passes_test
from .models import UserProfile

def list_books(request):
    books = Book.objects.all() 
    return render(request, "relationship_app/list_books.html", {"books": books})


# Class-based view using DetailView (as required)
class LibraryDetailView(DetailView):
    model = Library
    template_name = "relationship_app/library_detail.html"
    context_object_name = "library"

def register(request):
    """
    Registration using Django's built-in UserCreationForm.
    On success, logs the user in and redirects to the books list.
    """
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect("list_books")
    else:
        form = UserCreationForm()
    return render(request, "relationship_app/register.html", {"form": form})

# --- Role checks ---
def _has_role(user, required_role: str) -> bool:
    if not user.is_authenticated:
        return False
    try:
        return user.profile.role == required_role
    except UserProfile.DoesNotExist:
        return False


# --- Admin-only view ---
@user_passes_test(lambda u: _has_role(u, 'Admin'), login_url='login')
def admin_view(request):
    return render(request, "relationship_app/admin_view.html")


# --- Librarian-only view ---
@user_passes_test(lambda u: _has_role(u, 'Librarian'), login_url='login')
def librarian_view(request):
    return render(request, "relationship_app/librarian_view.html")


# --- Member-only view ---
@user_passes_test(lambda u: _has_role(u, 'Member'), login_url='login')
def member_view(request):
    return render(request, "relationship_app/member_view.html")
