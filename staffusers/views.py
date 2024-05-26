from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.utils import timezone

from library.models import Book
from users.models import BorrowRecord
from .forms import CreateBookForm, StaffUserCreationForm

User = get_user_model()


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user_type = request.POST.get('user_type')  # Get the user type from the hidden input
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_staff and user_type == 'staff':  # Check if the user is staff and user_type is 'staff'
                    login(request, user)
                    return redirect('staffusers:staff_home')
                else:
                    messages.error(request, 'Staff users should login from the staff login page.')
            else:
                messages.error(request, 'User not found')
        else:
            messages.error(request, 'Invalid username or password')
    else:
        form = AuthenticationForm()
    return render(request, 'staffusers/login.html', {'form': form})


@login_required
@user_passes_test(lambda u: u.is_staff)
def staff_home(request):
    books = Book.objects.all()
    return render(request, 'staffusers/index.html', {'books': books})


def add_book(request):
    if request.method == 'POST':
        form = CreateBookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('staffusers:staff_home')
    else:
        form = CreateBookForm()
    return render(request, 'staffusers/create_book.html', {'form': form})


def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        book.delete()
        return redirect('staffusers:staff_home')
    return render(request, 'staffusers/delete_book.html', {'book': book})


def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        form = CreateBookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('staffusers:staff_home')
    else:
        form = CreateBookForm(instance=book)
    return render(request, 'staffusers/edit_book.html', {'form': form})
