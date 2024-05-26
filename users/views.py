from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import DetailView
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test, login_required

from library.models import Book, BorrowRecord
from .forms import CustomUserCreationForm
from .models import BorrowedBook

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

    paginator = Paginator(books_list, 10)  # Show 10 books per page
    try:
        books = paginator.page(page)
    except PageNotAnInteger:
        books = paginator.page(1)
    except EmptyPage:
        books = paginator.page(paginator.num_pages)

    borrowed_books = BorrowedBook.objects.filter(user=request.user).values_list('book', flat=True)

    return render(request, 'users/index.html', {'books': books, 'borrowed_books': borrowed_books})


class BookDetailView(DetailView):
    model = Book
    template_name = 'users/book_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_borrowed'] = BorrowedBook.objects.filter(user=self.request.user, book=self.object).exists()
        context['available'] = self.object.quantity > 0
        return context


@login_required
def cancel_reservation(request, pk):
    book = get_object_or_404(Book, pk=pk)
    record = BorrowRecord.objects.filter(user=request.user, book=book).order_by(
        'borrowed_at').first()  # change this line
    if record:  # Checking if record is not None
        book.quantity += 1
        book.save()
        record.delete()
        messages.success(request, 'You have successfully cancelled your reservation.')
    else:
        messages.error(request, 'No reservation record found.')
    return redirect('users:book-detail', pk=pk)
