from django.contrib.auth.forms import UserCreationForm
from django import forms

class CustomUserCreationForm(UserCreationForm):
    """
    Custom user creation form that includes email field.
    """
    email = forms.EmailField(required=True, help_text='Required. Enter a valid email address.')
    class Meta:
        model = UserCreationForm.Meta.model
        fields = ('username', 'email', 'password1', 'password2')