from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test, login_required

from library.models import Book
from .forms import CustomUserCreationForm
from users.models import BorrowedBook, Reservation

User = get_user_model()


def index(request):
    return render(request, 'users/index.html')


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('users:index')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_staff:
                    messages.error(request, 'This is a staff user. Please use the staff login.')
                else:
                    login(request, user)
                    messages.success(request, 'You have successfully logged in.')
                    return redirect('users:index')
            else:
                messages.error(request, 'User not found.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})


@login_required
@user_passes_test(lambda u: not u.is_staff)
def users_home(request):
    if request.method == 'POST':
        book_id = request.POST.get('book_id')
        book = get_object_or_404(Book, id=book_id)
        BorrowedBook.objects.create(user=request.user, book=book)

    books_list = Book.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(books_list, 12)  # Show 10 books per page
    try:
        books = paginator.page(page)
    except PageNotAnInteger:
        books = paginator.page(1)
    except EmptyPage:
        books = paginator.page(paginator.num_pages)

    return render(request, 'users/index.html', {'books': books})


@login_required
def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    reservations = Reservation.objects.filter(user=request.user, book=book)
    available = book.quantity > 0
    remaining_time = None

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'reserve':
            if available and not reservations.exists():
                Reservation.objects.create(user=request.user, book=book)
                book.quantity -= 1
                book.save()
                messages.success(request, 'You have successfully reserved the book.')
            elif reservations.exists():
                messages.error(request, 'You have already reserved this book.')
            else:
                messages.error(request, 'This book is currently unavailable for reservation.')
        elif action == 'cancel':
            if reservations.exists():
                reservation = reservations.first()
                if not reservation.is_expired():
                    reservation.delete()
                    book.quantity += 1
                    book.save()
                    messages.success(request, 'You have successfully cancelled your reservation.')
                else:
                    messages.error(request, 'Your reservation has expired and cannot be cancelled.')
            else:
                messages.error(request, 'You have not reserved this book.')

    if reservations.exists():
        reservation = reservations.first()
        if not reservation.is_expired():
            remaining_time = timezone.timedelta(hours=24) - (timezone.now() - reservation.reserved_at)

    return render(request, 'users/book_detail.html', {
        'book': book,
        'reservations': reservations,
        'available': available,
        'remaining_time': remaining_time
    })
