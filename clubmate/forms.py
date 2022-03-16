from secrets import choice
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

from clubmate.models import Club, UserProfile


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('is_club_owner', 'picture',)


from clubmate.models import Rating


class RatingDetailForm(forms.ModelForm):
    title = forms.CharField(label='Title', max_length=30)
    # help_text="Please enter the rate title.")
    club = forms.ModelChoiceField(queryset=Club.objects.all(), required=True)
    rating_score = forms.FloatField(label='Rating Score',  # help_text="How much score would you give",
                                    initial=0.0, min_value=0.0, max_value=5.0, )
    is_safe = forms.BooleanField(label='Is it safe?',  # help_text="Do you think it is safe",
                                 initial=False, required=False)
    user_commentary = forms.CharField(label='Your Comment', max_length=9999,
                                      # help_text="Please enter the commentary here",
                                      widget=forms.Textarea(attrs={'rows': 3}))

    class Meta:
        model = Rating
        fields = ('title', 'club', 'rating_score', 'is_safe', 'user_commentary')


# class ClubForm(forms.ModelForm):
#     name = forms.CharField(max_length=30)
#     club_description = forms.CharField(max_length=999)
#     city = forms.CharField(max_length=30)
#     website_url = forms.URLField(max_length=200)
#     genre = forms.CharField(max_length=30)
#     # category = forms.CharField(max_length=30)
#     location_coordinates = forms.CharField(max_length=30, help_text='LNG LAT')  # Will need to be parsed as two floats
#     entry_fee = forms.FloatField(default=0.0)  # Minimum entry fee
#     opening_hours_week = forms.CharField(max_length=20)
#     opening_hours_weekend = forms.CharField(max_length=20)
#     # opening_hours = models.CharField(max_length=50)
#     picture = forms.ImageField(upload_to='club_pictures', default='club_pictures/default_club.png', blank=True)
#     covid_test_required = forms.BooleanField(default=False)
#     underage_visitors_allowed = forms.BooleanField(default=False)
#     average_rating = forms.FloatField(default=0.0, blank=True)
#     user_reported_safety = forms.BooleanField(default=False, blank=True)
#
#     class Meta:
#         model = Club
#         fields = ('name',)
