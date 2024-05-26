from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404
from django.contrib.auth import login, authenticate, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from users.models import BorrowRecord
from .forms import CreateBookForm

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


from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, redirect
from .forms import BorrowForm, ReturnBookForm
from library.models import Book, BorrowRecord
from django.utils import timezone


@login_required
def lend_book(request):
    borrow_form = BorrowForm(request.POST or None)

    if request.method == 'POST':
        if borrow_form.is_valid():
            borrow_instance = borrow_form.save(commit=False)

            existing_borrow_instance = BorrowRecord.objects.filter(
                book=borrow_instance.book,
                user=borrow_instance.user,
                returned_at__isnull=True
            ).first()

            if existing_borrow_instance:
                error_message = f"{borrow_instance.user} has already borrowed this book. Please return it before borrowing again."
                messages.error(request, error_message)
                return redirect('staffusers:lend_book')

            if borrow_instance.returned_at and borrow_instance.returned_at < borrow_instance.borrowed_at:
                error_message = 'Returned date cannot be before borrowed date.'
                context = {'borrow_form': borrow_form, 'error_message': error_message}
                return render(request, 'staffusers/staff_lend_book.html', context)

            with transaction.atomic():
                borrow_instance.save()
                borrow_instance.book.quantity -= 1
                borrow_instance.book.save()
                messages.success(request, 'Book has been successfully lent.')

                # Assuming you have a Reservation model or similar logic to cancel reservations
                # user_reservation = Reservation.objects.filter(
                #     book=borrow_instance.book,
                #     user=borrow_instance.user
                # ).first()

                # if user_reservation:
                #     user_reservation.delete()
                #     messages.info(request, 'Reservation has been automatically canceled.')

                return redirect('staffusers:lend_book')

    context = {'borrow_form': borrow_form}
    return render(request, 'staffusers/staff_lend_book.html', context)


@login_required
def lend_book(request):
    borrow_form = BorrowForm(request.POST or None)

    if request.method == 'POST':
        if borrow_form.is_valid():
            borrow_instance = borrow_form.save(commit=False)

            existing_borrow_instance = BorrowRecord.objects.filter(
                book=borrow_instance.book,
                user=borrow_instance.user,
                returned_at__isnull=True
            ).first()

            if existing_borrow_instance:
                error_message = f"{borrow_instance.user} has already borrowed this book. Please return it before borrowing again."
                messages.error(request, error_message)
                return redirect('staffusers:lend_book')

            if borrow_instance.returned_at and borrow_instance.returned_at < borrow_instance.borrowed_at:
                error_message = 'Returned date cannot be before borrowed date.'
                context = {'borrow_form': borrow_form, 'error_message': error_message}
                return render(request, 'staffusers/staff_lend_book.html', context)

            with transaction.atomic():
                borrow_instance.save()
                borrow_instance.book.quantity -= 1
                borrow_instance.book.save()
                messages.success(request, 'Book has been successfully lent.')

                # Assuming you have a Reservation model or similar logic to cancel reservations
                # user_reservation = Reservation.objects.filter(
                #     book=borrow_instance.book,
                #     user=borrow_instance.user
                # ).first()

                # if user_reservation:
                #     user_reservation.delete()
                #     messages.info(request, 'Reservation has been automatically canceled.')

                return redirect('staffusers:lend_book')

    context = {'borrow_form': borrow_form}
    return render(request, 'staffusers/staff_lend_book.html', context)


@login_required
def return_book(request):
    if request.method == 'POST':
        form = ReturnBookForm(request.POST)
        if form.is_valid():
            book = form.cleaned_data['book']
            user = form.cleaned_data['user']
            returning_date = form.cleaned_data['returning_date']

            try:
                borrow_record = BorrowRecord.objects.get(book=book, user=user, returned_at__isnull=True)

                borrow_record.returned_at = returning_date or timezone.now()
                borrow_record.save()

                book.quantity += 1
                book.save()
                messages.success(request, 'Book has been successfully marked as returned.')
            except BorrowRecord.DoesNotExist:
                messages.error(request, 'No matching borrow record found for the given book and user.')
            return redirect('staffusers:return_book')
    else:
        form = ReturnBookForm()

    return render(request, 'staffusers/staff_return_book.html', {'form': form})
