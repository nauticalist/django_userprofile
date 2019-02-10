from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User


class CreateUserForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = User
        fields = ('username', 'email', 'first_name', 'last_name',
                  'date_of_birth', 'bio', 'avatar', 'city', 'state',
                  'country', 'favorite_animal', 'hobbies', )


class UpdateUserForm(UserChangeForm):
    class Meta(UserChangeForm):
        model = User
        fields = ('username', 'email', 'first_name', 'last_name',
                  'date_of_birth', 'bio', 'avatar', 'city', 'state',
                  'country', 'favorite_animal', 'hobbies', )
