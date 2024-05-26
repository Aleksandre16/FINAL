from django import forms
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render

from library.models import Book, BorrowRecord
from staffusers.models import StaffUser
from users.models import User


class StaffUserCreationForm(UserCreationForm):
    position = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ['username', 'email', 'full_name', 'personal_number', 'date_of_birth', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_staff = True
        if commit:
            user.save()
            staff_user = StaffUser.objects.create(user=user, position=self.cleaned_data.get('position'))
        return user


class CreateBookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'authors', 'genre', 'pub_date', 'quantity']


@login_required
@user_passes_test(lambda u: StaffUser.objects.filter(user=u).exists())
def staff_home(request):
    return render(request, 'staffusers/index.html')


class BorrowForm(forms.ModelForm):
    class Meta:
        model = BorrowRecord
        fields = ['book', 'user']

    def __init__(self, *args, **kwargs):
        super(BorrowForm, self).__init__(*args, **kwargs)
        self.fields['book'].queryset = Book.objects.filter(quantity__gt=0)
        self.fields['user'].queryset = User.objects.filter(is_active=True)


class ReturnBookForm(forms.Form):
    book = forms.ModelChoiceField(queryset=Book.objects.all())
    user = forms.ModelChoiceField(queryset=User.objects.filter(is_active=True))
    returning_date = forms.DateTimeField(required=False)
