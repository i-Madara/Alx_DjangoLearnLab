from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import permission_required

@permission_required('bookshelf.can_view', raise_exception=True)
def view_books(request):
    return HttpResponse("You can view books!")

@permission_required('bookshelf.can_create', raise_exception=True)
def create_book(request):
    return HttpResponse("You can create a book!")

@permission_required('bookshelf.can_edit', raise_exception=True)
def edit_book(request):
    return HttpResponse("You can edit books!")

@permission_required('bookshelf.can_delete', raise_exception=True)
def delete_book(request):
    return HttpResponse("You can delete books!")
