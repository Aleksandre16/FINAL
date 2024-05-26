from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import CreateBookForm
from library.models import Book
from .forms import StaffUserCreationForm


def index(request):
    return render(request, 'staffusers/index.html')


def register(request):
    if request.method == 'POST':
        form = StaffUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('staffusers:index')  # You probably intended to do this.
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
                login(request, user)
                return redirect('staffusers:index')
    else:
        form = AuthenticationForm()
    return render(request, 'staffusers/login.html', {'form': form})


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


def edit_book(request, book_id):
    book = Book.objects.get(id=book_id)

    if request.method == "POST":
        form = CreateBookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('staffusers:index')
    else:
        form = CreateBookForm(instance=book)

    return render(request, 'staffusers/edit_book.html', {'form': form})


def delete_book(request, book_id):
    if request.method == "POST":
        book = Book.objects.get(id=book_id)
        book.delete()
        return redirect('staffusers:index')

    return render(request, 'staffusers/delete_book.html')


@login_required
@user_passes_test(lambda u: u.is_staff)
def staff_home(request):
    books = Book.objects.all()
    return render(request, 'staffusers/index.html', {'books': books})


@login_required
@user_passes_test(lambda u: u.is_staff)
def index(request):
    ...
