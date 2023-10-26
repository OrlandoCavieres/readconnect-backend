from django.forms import ModelForm

from Users.models import User


class RegisterModelForm(ModelForm):
    class Meta:
        model = User
        fields = ['email', 'password', 'name']


class UpdateUserModelForm(ModelForm):
    class Meta:
        model = User
        fields = ['name']
