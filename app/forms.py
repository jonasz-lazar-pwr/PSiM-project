from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import User, Comment


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = "Nazwa użytkownika:"
        self.fields['password'].label = "Hasło:"


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = "Nazwa użytkownika:"
        self.fields['password1'].label = "Hasło:"
        self.fields['password1'].help_text = ""
        self.fields['password2'].label = "Potwierdź hasło:"
        self.fields['password2'].help_text = ""


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment_text']
        labels = {
            'comment_text': 'Treść komentarza',
        }


class UploadQRCodeForm(forms.Form):
    qr_code_image = forms.ImageField()
