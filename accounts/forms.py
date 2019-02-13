from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import User

DATE_INPUT_FORMATS = ['%Y-%m-%d', '%m/%d/%Y', '%m/%d/%y']


class DateInput(forms.DateInput):
    input_type = 'date'
    format = DATE_INPUT_FORMATS


class CreateUserForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = User
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2')


class UpdateUserForm(UserChangeForm):
    password = None

    class Meta(UserChangeForm):
        model = User
        fields = ('email', 'first_name', 'last_name',
                  'date_of_birth', 'bio', 'avatar', 'city', 'state',
                  'country', 'favorite_animal', 'hobbies', )
        widgets = {
            'date_of_birth': DateInput()
        }

    def clean_bio(self):
        bio = self.cleaned_data['bio']
        if len(bio) < 10:
            raise forms.ValidationError(
                'Bio must be more than 10 characters!')
        return bio


class AvatarEditForm(forms.Form):
    x = forms.FloatField(widget=forms.HiddenInput())
    y = forms.FloatField(widget=forms.HiddenInput())
    width = forms.FloatField(widget=forms.HiddenInput())
    height = forms.FloatField(widget=forms.HiddenInput())
    rotate = forms.FloatField(widget=forms.HiddenInput())
    scaleX = forms.FloatField(widget=forms.HiddenInput())
    scaleY = forms.FloatField(widget=forms.HiddenInput())
