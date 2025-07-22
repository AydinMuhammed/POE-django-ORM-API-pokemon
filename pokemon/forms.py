from django import forms
from django.contrib.auth import authenticate

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, label="username")
    password = forms.CharField(max_length=100, widget=forms.PasswordInput, label="password")

    def clean(self):
        cleaned_data = super().clean()
        # Check that the credentials are correct
        # If username or password is incorrect, authenticate returns None
        # If username and password are correct, authenticate returns the user
        user = authenticate(username=cleaned_data.get('username'), password=cleaned_data.get('password'))
        # after validation, ad a user attribute to the form object so the view can use it
        self.user = user
        if user is None:
            raise forms.ValidationError("Incorrect username or password")
        return cleaned_data