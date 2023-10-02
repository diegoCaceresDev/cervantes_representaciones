"""Users forms."""

# Django
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CustomUserCreationForm(UserCreationForm):
    """
    El modelo de formulario de creación de usuario personalizado.
    Este modelo herea de UserCreationForm y agrega un campo de correo
    electrónico.

    Args:
        UserCreationForm (UserCreationForm): Formulario de creación de usuario
        de Django.

    Returns:
        User: Modelo de usuario de Django.
    """

    email = forms.EmailField(required=True)

    class Meta:
        """Meta options."""

        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        """Save form."""

        user = super(CustomUserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]

        if commit:
            user.save()
        return user

    def clean_email(self):
        """Clean email."""

        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(message="El correo ya existe, intente con otro")
        return email
