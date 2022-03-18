from multiprocessing import context
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse
from clubmate.models import Club, UserProfile, Rating
from django.contrib.auth import login, authenticate, logout
from clubmate.forms import UserForm, UserProfileForm
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import render_to_response
from clubmate.forms import RatingDetailForm

from django.core.paginator import Paginator
from . import models
from .models import Club

# Push
def permissions_check_clubmate_user(request, context_dict):
    """ Helper method to check user permissions. """
    if not request.user.is_anonymous:
        user = request.user  # Get user from the request
        clubmate_user = UserProfile.objects.get_or_create(user=user)[0]  # Map it to our user
        context_dict['clubmate_user'] = clubmate_user


def index(request):
    clubs = Club.objects.all()
    context_dict = {'clubs': clubs}
    permissions_check_clubmate_user(request, context_dict)
    return render(request, 'clubmate/index.html', context=context_dict)


def about(request):
    context_dict = {}
    permissions_check_clubmate_user(request, context_dict)
    return render(request, 'clubmate/about.html', context=context_dict)


def discover(request):
    all_clubs = sorted(Club.objects.all(), key=lambda c: c.average_rating_, reverse=True)
    clubs_by_rating = sorted(Club.objects.all(), key=lambda c: c.average_rating_, reverse=True)[:3]  # High to low
    safe_clubs = sorted(Club.objects.all(), key=lambda c: c.user_reported_safety_)[:3]
    cheapest_clubs = Club.objects.order_by('entry_fee')[:3]
    context_dict = {'all_clubs': all_clubs, 'clubs_by_rating': clubs_by_rating, 'safe_clubs': safe_clubs,
                    'cheapest_clubs': cheapest_clubs}
    permissions_check_clubmate_user(request, context_dict)
    return render(request, 'clubmate/discover.html', context=context_dict)


def club_detail(request, club_id):
    try:
        club = Club.objects.get(id=club_id)
    except Club.DoesNotExist:
        club = None
    context_dict = {'club': club}
    permissions_check_clubmate_user(request, context_dict)
    return render(request, 'clubmate/club_detail.html', context=context_dict)


def ratings(request):
    # use for reverse
    all_rating_by_time = sorted(Rating.objects.all(), key=lambda c: c.posted_at, reverse=True)
    all_rating_by_upvote = sorted(Rating.objects.all(), key=lambda c: c.number_of_upvotes, reverse=True)

    # use for not reverse
    reverse_rating_by_time = sorted(Rating.objects.all(), key=lambda c: c.posted_at, reverse=False)
    reverse_rating_by_upvote = sorted(Rating.objects.all(), key=lambda c: c.number_of_upvotes, reverse=False)

    paginator_time = Paginator(all_rating_by_time, 3)
    paginator_upvote = Paginator(all_rating_by_upvote, 3)

    reverse_paginator_time = Paginator(reverse_rating_by_time, 3)
    reverse_paginator_upvote = Paginator(reverse_rating_by_upvote, 3)

    page_number = request.GET.get('page')
    page_object_time = paginator_time.get_page(page_number)
    page_object_upvote = paginator_upvote.get_page(page_number)

    page_reverse_object_time = reverse_paginator_time.get_page(page_number)
    page_reverse_object_upvote = reverse_paginator_upvote.get_page(page_number)

    context_dict = {'page_object_time': page_object_time, 'page_object_upvote': page_object_upvote,
                    'reverse_rating_by_time': page_reverse_object_time,
                    'reverse_rating_by_upvote': page_reverse_object_upvote}
    permissions_check_clubmate_user(request, context_dict)
    return render(request, 'clubmate/ratings.html', context_dict)


def rating_detail(request, rating_id):
    try:
        rating = Rating.objects.get(id=rating_id)
    except Rating.DoesNotExist:
        rating = None
    context_dict = {'rating': rating}
    permissions_check_clubmate_user(request, context_dict)
    return render(request, 'clubmate/rating_detail.html', context=context_dict)


@login_required  # Anonymous users never even get access to this URL / Restrict to students
def rate(request):
    if request.method == 'POST':
        form = RatingDetailForm(request.POST)
        user = request.user
        if form.is_valid():
            rating = form.save(commit=False)
            user = UserProfile.objects.get(user=user)
            rating.author = user
            rating.save()
            return redirect(reverse("clubmate:index"))
        else:
            return HttpResponse("Something went wrong.")
    else:
        form = RatingDetailForm()
        context_dict = {'form': form}
        return render(request, 'clubmate/rate_club.html',
                      context=context_dict)  # The template that was there before was incorrect


@login_required  # Anonymous users never even get access to this URL / Restrict to students
def rate_detail(request, club_id):
    form = RatingDetailForm()
    club = Club.objects.get_or_create(id=club_id)[0]

    if request.method == 'POST':
        form = RatingDetailForm(request.POST)
        user = request.user
        user_pro = UserProfile.objects.get(user=user)
        this_club = Club.objects.get(id=club_id)
        if form.is_valid():
            if this_club:
                this_rate = form.save(commit=False)
                this_rate.author = user_pro
                this_rate.club = this_club
                this_rate.save()
                return redirect(reverse("clubmate:ratings"))
        else:
            print(form.errors)
    context_dict = {'club_id': club_id, 'form': form, 'club': club}

    return render(request, 'clubmate/rate_club_detail.html', context_dict)


@login_required  # Anonymous users never even get access to this URL
def upvote_rating(request, rating_id):
    rating = Rating.objects.get(id=rating_id)  # Get the rating to be modified
    rating.number_of_upvotes += 1  # Increment the number of votes
    rating.save()
    return HttpResponseRedirect(
        request.META.get('HTTP_REFERER'))  # Redirects to the same page. TODO: Try handling with AJAX?


@login_required  # Anonymous users never even get access to this URL
def save_club(request, club_id):
    club = Club.objects.get(id=club_id)  # Get the club in question
    user = request.user  # Get the current user
    clubmate_user = UserProfile.objects.get_or_create(user=user)[0]
    clubmate_user.clubs.add(club)  # Add it to the user's profile
    return redirect(reverse('clubmate:profile', kwargs={'username': user.username}))  # Redirect to profile


@login_required  # Restrict to club owner
def add_club(request):
    user = request.user
    clubmate_user = UserProfile.objects.get_or_create(user=user)[0]  # FIX: Must add it to the user's profile

    if request.method == 'POST':
        new_club_name = request.POST.get('name')
        new_club_description = request.POST.get('club_description')
        new_entry_fee = request.POST.get('entry_fee')
        new_opening_hours_week = request.POST.get('opening_hours_week')
        new_opening_hours_weekend = request.POST.get('opening_hours_weekend')
        new_category = request.POST.get('genre')
        new_covid_test_required = request.POST.get('covid_test_required')
        new_underage_visitors_allowed = request.POST.get('underage_visitors_allowed')
        new_website_url = request.POST.get('website_url')
        new_location_coordinates = request.POST.get('location_coordinates')
        new_picture = request.FILES.get('picture')
        if new_covid_test_required == None:
            new_covid_test_required = 0
        if new_underage_visitors_allowed == None:
            new_underage_visitors_allowed = 0
        Club.objects.create(name=new_club_name,
                            club_description=new_club_description,
                            entry_fee=new_entry_fee,
                            opening_hours_week=new_opening_hours_week,
                            opening_hours_weekend=new_opening_hours_weekend,
                            genre=new_category,
                            covid_test_required=new_covid_test_required,
                            underage_visitors_allowed=new_underage_visitors_allowed,
                            website_url=new_website_url,
                            location_coordinates=new_location_coordinates,
                            picture=new_picture)
        club = Club.objects.get(name=new_club_name)  # Get the club
        clubmate_user.clubs.add(club)  # FIX: Add newly created club to the club owner's profile
        return render(request, 'clubmate/operation_successful.html')
    else:
        return render(request, 'clubmate/add_club.html')


@login_required
def profile(request, username):
    user = User.objects.get(username=username)  # Match username from the default user
    clubmate_user = UserProfile.objects.get_or_create(user=user)[0]  # Match it with our custom user
    rating_list = Rating.objects.filter(author=clubmate_user)
    context_dict = {'clubmate_user': clubmate_user, 'ratingList': rating_list}
    return render(request, 'clubmate/profile.html', context=context_dict)


@login_required  # Restrict to club owner
def edit_club(request, club_id):
    club = Club.objects.get(id=club_id)
    if request.user != UserProfile.is_club_owner:
        return HttpResponse("Sorry, you have no right to edit this club.")

    # if request.method == "POST":
    #     new_club_name = request.POST.get('name')
    #     new_club_description = request.POST.get('club_description')
    #     new_entry_fee = request.POST.get('entry_fee')
    #     new_opening_hours_week = request.POST.get('opening_hours_week')
    #     new_opening_hours_weekend = request.POST.get('opening_hours_weekend')
    #     new_category = request.POST.get('genre')
    #     new_covid_test_required = request.POST.get('covid_test_required')
    #     new_underage_visitors_allowed = request.POST.get('underage_visitors_allowed')
    #     new_website_url = request.POST.get('website_url')
    #     new_location_coordinates = request.POST.get('location_coordinates')
    #     new_picture = request.POST.get('picture')
    #     club.name = new_club_name
    #     club.club_description = new_club_description
    #     club.entry_fee = new_entry_fee
    #     club.opening_hours_week = new_opening_hours_week
    #     club.opening_hours_weekend = new_opening_hours_weekend
    #     club.genre = new_category
    #     club.covid_test_required = new_covid_test_required
    #     club.underage_visitors_allowed = new_underage_visitors_allowed
    #     club.website_url = new_website_url
    #     club.location_coordinates = new_location_coordinates
    #     club.picture = new_picture
    #     club.save()
    #     return redirect("clubmate:club_detail", id=id)
    # else:
    #     context_dict = {'club': club}
    #     return render(request, 'clubmate/edit_club.html', context_dict)


@login_required  # Restrict to club owner
def delete_club(request, club_id):
    club = Club.objects.get(id=club_id)
    if request.user != UserProfile.is_club_owner:
        return HttpResponse("Sorry, you have no right to delete this club.")
    else:
        club.delete()
        return redirect('clubmate:discover')


@login_required  # Restrict to students
def edit_rating(request, rating_id):
    rating = Rating.objects.get(id=rating_id)  # Get the rating

    if request.method == 'POST':
        user = request.user
        new__title = request.POST.get('title')
        new_score = request.POST.get('rating_score')
        new_safe = request.POST.get('is_safe')
        new_rating = request.POST.get('user_commentary')
        rating.title = new__title
        rating.rating_score = new_score
        rating.is_safe = new_safe
        rating.user_commentary = new_rating
        rating.save()
        return redirect((reverse('clubmate:profile', kwargs={'username': user.username})))
    else:
        context_dict = {'rating': rating}
        return render(request, 'clubmate/edit_rating.html', context_dict)


@login_required  # Restrict to students
def delete_rating(request, rating_id):
    rating = Rating.objects.filter(id=rating_id)
    user = request.user
    rating.delete()
    return redirect(reverse('clubmate:profile', kwargs={'username': user.username}))


def log_in(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                # Redirect to index page.
                return redirect(reverse("clubmate:index"))
            else:
                # Return a 'disabled account' error message
                return HttpResponse("Your account is disabled.")
        else:
            # Return an 'invalid login' error message.
            print("invalid login details " + username + " " + password)
    else:
        # the login is a  GET request, so just show the user the login form.
        return render(request, 'clubmate/login.html')


@login_required
def log_out(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect(reverse("clubmate:index"))


def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()

            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'clubmate/register.html',
                  context={'user_form': user_form, 'profile_form': profile_form, 'registered': registered})
