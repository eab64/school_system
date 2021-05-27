from django.contrib.auth import password_validation
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .widget import FengyuanChenDatePickerInput
from django import forms
from django.utils.translation import gettext_lazy as _


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'last_name']


class TeacherForm(forms.Form):
    name = forms.CharField(label='name', max_length=20)
    surname = forms.CharField(label='surname', max_length=20)
    subject = forms.CharField(label='subject', max_length=20)
    salary = forms.IntegerField(label='salary')


class StudentForm(forms.Form):
    name = forms.CharField(label='name', max_length=20)
    surname = forms.CharField(label='surname', max_length=20)
    score = forms.IntegerField(label='score')

from django import forms

class DateForm(forms.Form):
    date = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M'])

class LessonForm(forms.Form):
    classs = forms.CharField(label='class', max_length=20)
    subject = forms.CharField(label='subject', max_length=20)
    date = forms.DateTimeField(
        input_formats=['%d/%m/%Y %H:%M'],
        widget=FengyuanChenDatePickerInput())
    room = forms.IntegerField(label='room')


class SectionsForm(forms.Form):
    klass = forms.CharField(label='class', max_length=20)
    subject = forms.CharField(label='subject', max_length=20)
    date = forms.DateTimeField()
    room = forms.IntegerField(label='room')


class BookForm(forms.Form):
    name = forms.CharField(label='name', max_length=255)


class BookGiveForm(forms.Form):
    name = forms.CharField(label='name', max_length=20)
    surname = forms.CharField(label='surname', max_length=20)
    classs = forms.CharField(label='class', max_length=20)
    book = forms.IntegerField(label='book')


class SubjectForm(forms.Form):
    name = forms.CharField(label='name', max_length=100)


#
# class CreateUserForm(UserCreationForm):
#     PLANNING_CHOICES = (
#         ('0', u'Скидка 30%'),
#         ('1', u'Без скидки'),
#     )
#     username = forms.CharField(max_length=12, min_length=4, required=True, help_text='Required: First Name',
#                                 widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}))
#     surname = forms.CharField(max_length=12, min_length=4, required=True, help_text='Required: Surname',
#                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Surname'}))
#     email = forms.EmailField(max_length=50, help_text='Required. Inform a valid email address.',
#                              widget=(forms.TextInput(attrs={'class': 'form-control'})))
#     password1 = forms.CharField(label=('Password'),
#                                 widget=(forms.PasswordInput(attrs={'class': 'form-control'})),
#                                 help_text=password_validation.password_validators_help_text_html())
#     password2 = forms.CharField(label=_('Password Confirmation'),
#                                 widget=forms.PasswordInput(attrs={'class': 'form-control'}),
#                                 help_text=_('Just Enter the same password, for confirmation'))
#
#     # planning = forms.ChoiceField(required=True, choices=PLANNING_CHOICES)
#     class Meta(UserCreationForm.Meta):
#         model = User
#         fields = UserCreationForm.Meta.fields + ('username', 'surname', 'email', 'password1', 'password2')


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=12, min_length=4, required=True, help_text='Required: First Name',
                                 widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=12, min_length=4, required=True, help_text='Required: Last Name',
                                widget=(forms.TextInput(attrs={'class': 'form-control'})))
    email = forms.EmailField(max_length=50, help_text='Required. Inform a valid email address.',
                             widget=(forms.TextInput(attrs={'class': 'form-control'})))
    password1 = forms.CharField(label=_('Password'),
                                widget=(forms.PasswordInput(attrs={'class': 'form-control'})),
                                help_text=password_validation.password_validators_help_text_html())
    password2 = forms.CharField(label=_('Password Confirmation'),
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                                help_text=_('Just Enter the same password, for confirmation'))
