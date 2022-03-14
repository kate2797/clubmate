from django import forms
from clubmate.models import Rating


class RatingDetailForm(forms.ModelForm):
    title = forms.CharField(max_length=30,
                            help_text="Please enter the rate title.")
    rating_score = forms.FloatField(widget=forms.HiddenInput(), initial=0.0)
    is_safe = forms.BooleanField(widget=forms.HiddenInput(), initial=False)
    user_commentary = forms.CharField(max_length=9999,
                                      help_text="Please enter the commentary here")

    class Meta:
        model = Rating
        exclude = ('author', 'club')
