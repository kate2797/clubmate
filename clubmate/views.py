from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


# We will likely need views for: login, logout, register
# based on if we are using some out-of-the-box solution or not (K).

def index(request):
    return render(request, 'clubmate/index.html')


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
    pass  # Add appropriate template


@login_required
def profile(request, username):
    pass  # Add appropriate template


@staff_member_required
def edit_club(request, club_id):
    pass  # Add appropriate template


@staff_member_required
def delete_club(request, club_id):
    pass  # Add appropriate template


@login_required
def edit_rating(request, rating_id):
    pass  # Add appropriate template


@login_required
def delete_rating(request, rating_id):
    pass  # Add appropriate template
