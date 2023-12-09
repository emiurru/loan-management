from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from perfiles.models import Avatar


class UserRegisterForm(UserCreationForm):
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repetir contraseña', widget=forms.PasswordInput)

    dni = forms.CharField(required=True)

    class Meta:
       model = User
       fields = ['last_name', 'first_name', 'dni', 'username', 'email', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):

   class Meta:
       model = User
       fields = ['last_name', 'first_name', 'email']

class AvatarFormulario(forms.ModelForm):
    class Meta:
        model = Avatar
        fields = ['imagen']