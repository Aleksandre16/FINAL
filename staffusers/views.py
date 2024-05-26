from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

from library.models import Book
from .forms import CreateBookForm, StaffUserCreationForm

User = get_user_model()


def index(request):
    return render(request, 'staffusers/index.html')


def register(request):
    if request.method == 'POST':
        form = StaffUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('staffusers:staff_home')  # Redirect to staff home page
    else:
        form = StaffUserCreationForm()
    return render(request, 'staffusers/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_staff:
                    if 'staff' in request.POST:  # Check if staff button was clicked
                        login(request, user)
                        return redirect('staffusers:staff_home')  # Redirect to staff home page
                    else:
                        messages.error(request, 'Staff users should login from the staff login page.')
                else:
                    if 'user' in request.POST:  # Check if user button was clicked
                        login(request, user)
                        return redirect('users:index')  # Redirect to regular user index page
                    else:
                        messages.error(request, 'Regular users should login from the regular user login page.')
            else:
                messages.error(request, 'User not found')
        else:
            messages.error(request, 'Invalid username or password')
    else:
        form = AuthenticationForm()
    return render(request, 'staffusers/login.html', {'form': form})


@login_required
@user_passes_test(lambda u: u.is_staff)
def create_book(request):
    if request.method == "POST":
        form = CreateBookForm(request.POST)
        if form.is_valid():
            # here save will directly create the book in the database
            form.save()
            return redirect('staffusers:index')
    else:
        form = CreateBookForm()

    return render(request, 'staffusers/create_book.html', {'form': form})


@login_required
@user_passes_test(lambda u: u.is_staff)
def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if request.method == "POST":
        form = CreateBookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('staffusers:index')
    else:
        form = CreateBookForm(instance=book)

    return render(request, 'staffusers/edit_book.html', {'form': form})


@login_required
@user_passes_test(lambda u: u.is_staff)
def delete_book(request, book_id):
    if request.method == "POST":
        book = get_object_or_404(Book, id=book_id)
        book.delete()
        return redirect('staffusers:index')

    return render(request, 'staffusers/delete_book.html')


@login_required
@user_passes_test(lambda u: u.is_staff)
def staff_home(request):
    books = Book.objects.all()
    return render(request, 'staffusers/index.html', {'books': books})
