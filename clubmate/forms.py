from django import forms
from django.contrib.auth.models import User

from clubmate.models import Club, UserProfile, Rating


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('is_club_owner', 'picture',)


class RatingDetailForm(forms.ModelForm):
    title = forms.CharField(label='Title', max_length=30)
    club = forms.ModelChoiceField(queryset=Club.objects.all(), required=True)
    rating_score = forms.FloatField(label='Rating Score', initial=0.0, min_value=0.0, max_value=5.0, )
    is_safe = forms.BooleanField(label='Is it safe?', initial=False, required=False)
    user_commentary = forms.CharField(label='Your Comment', max_length=9999, widget=forms.Textarea(attrs={'rows': 3}))

    class Meta:
        model = Rating
        fields = ('title', 'club', 'rating_score', 'is_safe', 'user_commentary')


class RateDetailForm(forms.ModelForm):
    title = forms.CharField(label='Title', max_length=30)

    rating_score = forms.FloatField(label='Rating Score', initial=0.0, min_value=0.0, max_value=5.0, )
    is_safe = forms.BooleanField(label='Is it safe?', initial=False, required=False)
    user_commentary = forms.CharField(label='Your Comment', max_length=9999, widget=forms.Textarea(attrs={'rows': 3}))

    class Meta:
        model = Rating
        fields = ('title', 'rating_score', 'is_safe', 'user_commentary')
