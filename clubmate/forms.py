from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from clubmate.models import UserProfile

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)

class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ('club_owner','picture',)