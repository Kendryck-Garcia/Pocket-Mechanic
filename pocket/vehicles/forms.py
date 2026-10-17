from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class AccessibleErrorsMixin:
    """Mark invalid fields with aria-invalid and point them at their error text."""

    def full_clean(self):
        super().full_clean()
        for name in self.errors:
            if name in self.fields:
                field = self[name]
                field.field.widget.attrs.update({
                    "aria-invalid": "true",
                    "aria-describedby": f"{field.id_for_label}-error",
                })


class CreateUserForm(AccessibleErrorsMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class LoginForm(AccessibleErrorsMixin, AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"autocomplete": "username"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}))
