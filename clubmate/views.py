from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render

from clubmate.models import Club, UserProfile


def index(request):
    return render(request, 'clubmate/index.html')


def about(request):
    pass  # Add appropriate template


def discover(request):
    all_clubs = Club.objects.all()
    clubs_by_rating = sorted(Club.objects.all(), key=lambda c: c.average_rating, reverse=True)[:3]  #  Ordering high to low
    safe_clubs = sorted(Club.objects.all(), key=lambda c: c.user_reported_safety)[:3]
    cheapest_clubs = Club.objects.order_by('entry_fee')[:3]
    context = {'all_clubs': all_clubs, 'clubs_by_rating': clubs_by_rating, 'safe_clubs': safe_clubs, 'cheapest_clubs': cheapest_clubs}
    return render(request, 'clubmate/discover.html', context=context)


def club_detail(request, club_id):
    try:
        club = Club.objects.get(pk=club_id)
    except Club.DoesNotExist:
        club = None
    context = {'club': club}
    return render(request, 'clubmate/club_detail.html', context=context)


def ratings(request):
    pass  # Add appropriate template


def rating_detail(request, rating_id):
    pass  # Add appropriate template


@login_required
def rate(request):
    return render(request, 'clubmate/edit_rating.html')


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
    return render(request, 'clubmate/edit_rating.html')


@login_required
def delete_rating(request, rating_id):
    return render(request, 'clubmate/delete_rating.html')
