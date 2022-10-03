from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.db import models
from admin_data.models import WebUser


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField()
    last_name = forms.CharField()

    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('A user has already registered using this email')
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError('A user has already registered using this username')
        return username


class WebUserForm(ModelForm):
    class Meta:
        model = WebUser
        fields = ('justification',)


class ContactForm(forms.Form):
    name = forms.CharField(required=True, max_length=50)
    subject = forms.CharField(required=True, max_length=50)
    message = forms.CharField(widget=forms.Textarea)
    email_address = forms.EmailField(required=True, max_length=50)
