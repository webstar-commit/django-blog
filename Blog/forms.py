from django import forms
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm

from .models import *


class RegistrationForm(UserCreationForm):
    email = models.CharField()

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        user.password1 = self.cleaned_data['password1']
        user.password2 = self.cleaned_data['password2']

        if commit:
            user.save()

        return user


class commentform(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)


class replyform(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ('body',)


class UserLogin(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = forms.CharField()
        password = forms.CharField(widget=forms.PasswordInput)
        user = authenticate(username=username, password=password)
        if user is not None:
            raise forms.ValidationError("Your are not registered")
        if not user.check_password(password):
            raise forms.ValidationError("password error")
        if not user.check_username(username):
            raise forms.ValidationError("error username")
        return super(UserLogin, self).clean(*args, **kwargs)



