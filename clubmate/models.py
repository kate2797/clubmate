from django.contrib.auth.models import User
from django.db import models
from django.db.models import Avg
from django.core.validators import MaxValueValidator, MinValueValidator
from django.urls import reverse


class Club(models.Model):
    name = models.CharField(max_length=30)
    club_description = models.TextField()
    city = models.CharField(max_length=30)
    website_url = models.URLField()
    genre = models.CharField(max_length=30)
    location_coordinates = models.CharField(max_length=30, help_text='LNG LAT')  # Will need to be parsed as two floats
    entry_fee = models.FloatField(default=0.0)  # Minimum entry fee
    opening_hours_week = models.CharField(max_length=20)
    opening_hours_weekend = models.CharField(max_length=20)
    picture = models.ImageField(upload_to='club_pictures', default='club_pictures/default_club.png', blank=True)
    covid_test_required = models.BooleanField(default=0)
    underage_visitors_allowed = models.BooleanField(default=0)
    average_rating = models.FloatField(default=0.0, blank=True)
    user_reported_safety = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('clubmate:club_detail', args=[self.id])

    @property
    def average_rating_(self):
        return self.ratings_list.aggregate(Avg('rating_score'))['rating_score__avg']  # Order by on-the-fly in views

    @property
    def user_reported_safety_(self):
        safe_count = self.ratings_list.filter(is_safe=True).count()
        unsafe_count = self.ratings_list.filter(is_safe=False).count()
        return "SAFE" if safe_count > unsafe_count else "UNSAFE"

    # def save(self, *args, **kwarg):
    #     self.average_rating = self.average_rating_
    #     self.user_reported_safety = self.user_reported_safety_
    #     super(Club, self).save(*args, **kwarg)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='profile_pictures', default='profile_pictures/default_user.png', blank=True)
    bio = models.CharField(max_length=100, blank=True)
    clubs = models.ManyToManyField(Club, blank=True)  # Storing the clubs users saved/added
    is_club_owner = models.BooleanField(help_text="Tick this if you're a club owner", null=True)

    def __str__(self):
        return self.user.username


class Event(models.Model):
    title = models.CharField(max_length=30)
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='events_list')
    picture = models.ImageField(upload_to='event_pictures', default='event_pictures/default_event.png', blank=True)
    happening_at = models.DateTimeField(help_text='MM/DD/YY HH:MM')
    capacity = models.IntegerField(default=0)

    class Meta:
        ordering = ['happening_at']  # Default ordering is most recent to the least recent

    def __str__(self):
        return self.title


class Rating(models.Model):
    title = models.CharField(max_length=30)
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='ratings_list')
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='ratings_written_list')
    rating_score = models.FloatField(default=0.0,
                                     validators=[MinValueValidator(1.0), MaxValueValidator(5.0)])  # Validate
    is_safe = models.BooleanField(default=False)
    user_commentary = models.TextField()
    posted_at = models.DateTimeField(auto_now_add=True)
    number_of_upvotes = models.IntegerField(default=0)
    user_reported_safety = models.BooleanField(default=False, blank=True)

    @property
    def user_reported_safety_(self):
        return "SAFE" if self.is_safe is True else "UNSAFE"

    # def save(self, *args, **kwarg):
    #     self.user_reported_safety = self.user_reported_safety_
    #     super(Rating, self).save(*args, **kwarg)

    class Meta:
        ordering = ['-number_of_upvotes']  # Default ordering is high to low

    def __str__(self):
        return self.title
