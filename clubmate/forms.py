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
from clubmate.models import Rating


class RatingDetailForm(forms.ModelForm):
    title = forms.CharField(max_length=30,
                            help_text="Please enter the rate title.")
    rating_score = forms.FloatField(help_text="How many score you want to give", initial=0.0)
    is_safe = forms.BooleanField(help_text="Do you think it is safe", initial=False)
    user_commentary = forms.CharField(max_length=9999,
                                      help_text="Please enter the commentary here")

    class Meta:
        model = Rating
        exclude = ('author', 'club', 'posted_at', 'number_of_upvotes', 'user_reported_safety')
