from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render

from clubmate.models import Club, UserProfile


def index(request):
    clubs = sorted(Club.objects.all(), key=lambda c: c.average_rating, reverse=True)  # Ordering high to low
    context = {'clubs': clubs}
    return render(request, 'clubmate/index.html', context=context)


def about(request):
    pass  # Add appropriate template


def discover(request):
    return render(request, 'clubmate/discover.html')


def club_detail(request, club_id):
    return render(request, 'clubmate/club_detail.html')


def ratings(request):
    pass  # Add appropriate template


def rating_detail(request, rating_id):
    pass  # Add appropriate template


@login_required
def rate(request):
    pass  # Add appropriate template


@staff_member_required
def add_club(request):
    return render(request, 'clubmate/add_club.html')


@login_required
def profile(request, username):
    user = User.objects.get(username=username)  # Match username from the default user
    clubmate_user = UserProfile.objects.get(user=user)  # Match it with our custom user
    context = {'clubmate_user': clubmate_user}
    return render(request, 'clubmate/profile.html', context=context)


@staff_member_required
def edit_club(request, club_id):
    return render(request, 'clubmate/edit_club.html')


@staff_member_required
def delete_club(request, club_id):
    return render(request, 'clubmate/delete_club.html')


@login_required
def edit_rating(request, rating_id):
    pass  # Add appropriate template


@login_required
def delete_rating(request, rating_id):
    pass  # Add appropriate template
