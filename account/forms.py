from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser
from django.utils.translation import gettext_lazy as _


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password1"].error_messages = {
            "required": "Şifrə sahəsi boş ola bilməz.",
            "min_length": "Şifrənin uzunluğu ən azı 8 simvol olmalıdır.",
        }
        self.fields["password2"].error_messages = {
            "required": "Şifrə təsdiqi sahəsi boş ola bilməz.",
            "password_mismatch": "Şifrələr uyğun gəlmir.",
        }
        self.fields["username"].error_messages = {
            "required": "İstifadəçi adı sahəsi boş ola bilməz.",
            "unique": "Bu istifadəçi adı artıq qeydiyyatdan keçib.",
        }
        self.fields["email"].error_messages = {
            "required": "E-poçt sahəsi boş ola bilməz.",
            "invalid": "Zəhmət olmasa düzgün bir e-poçt ünvanı daxil edin.",
            "unique": "Bu e-poçt ünvanı artıq qeydiyyatdan keçib.",
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Şifrələr uyğun gəlmir.")
        return password2

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if username.isdigit():
            raise forms.ValidationError(
                "İstifadəçi adı yalnızca rəqəmlərdən ibarət ola bilməz."
            )
        return username


class CustomAuthenticationForm(AuthenticationForm):
    error_messages = {
        "invalid_login": _("İstifadəçi adı və ya şifrə yanlışdır."),
        "inactive": _("Hesabınız aktiv deyil."),
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].required = True
        self.fields["password"].required = True
        self.fields["username"].error_messages = {
            "required": _("İstifadəçi adı boş ola bilməz.")
        }
        self.fields["password"].error_messages = {
            "required": _("Şifrə boş ola bilməz.")
        }
