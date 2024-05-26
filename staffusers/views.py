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


@login_required
def borrow_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if book.quantity > 0:
        book.quantity -= 1  # Decrease the book count by 1
        book.save()  # Don't forget to save the changes
        BorrowRecord.objects.create(user=request.user, book=book)
        messages.success(request, 'You have successfully borrowed this book.')
    else:
        messages.error(request, 'This book is currently unavailable.')
    return redirect('users:book-detail', pk=pk)  # redirect to the book detail view in users app


@login_required
def return_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    record = get_object_or_404(BorrowRecord, book=book, user=request.user, returned_at__isnull=True)
    record.returned_at = timezone.now()
    record.save()
    book.quantity += 1
    book.save()
    return redirect('book-detail', pk=pk)
