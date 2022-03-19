import time

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core import serializers
from django.shortcuts import render, redirect
from django.urls import reverse
from clubmate.models import UserProfile, Rating, Club
from django.contrib.auth import login, authenticate, logout
from clubmate.forms import UserForm, UserProfileForm, RatingDetailForm, RateDetailForm
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.core.paginator import Paginator


def permissions_check_clubmate_user(request, context_dict):
    """ Helper method to allow rendering of content based on user permissions within templates by passing our custom
    user into the context dictionary. """
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
    default_sorting = serializers.serialize("json", all_clubs)  # For JavaScript
    default_sorting_reverse = serializers.serialize("json", sorted(Club.objects.all(), key=lambda c: c.average_rating_))
    context_dict = {'all_clubs': all_clubs, 'clubs_by_rating': clubs_by_rating, 'safe_clubs': safe_clubs,
                    'cheapest_clubs': cheapest_clubs, 'default_sorting': default_sorting,
                    'default_sorting_reverse': default_sorting_reverse}
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
            return redirect(reverse("clubmate:ratings"))
        else:
            return HttpResponse("Something went wrong.")
    else:
        form = RatingDetailForm()
        context_dict = {'form': form}
        return render(request, 'clubmate/rate_club.html',
                      context=context_dict)  # The template that was there before was incorrect


@login_required  # Anonymous users never even get access to this URL / Restrict to students
def rate_detail(request, club_id):
    form = RateDetailForm()
    try:
        club = Club.objects.get(id=club_id)
    except Club.DoesNotExist:
        club = None

    if request.method == 'POST':
        form = RateDetailForm(request.POST)
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
    time.sleep(3)
    return redirect(reverse('clubmate:profile', kwargs={'username': user.username}))  # Redirect to profile


@login_required  # Restrict to club owner
def add_club(request):
    if request.method == 'POST':
        new_club_name = request.POST.get('name')
        new_club_description = request.POST.get('club_description')
        new_city = request.POST.get('city')
        new_website_url = request.POST.get('website_url')
        new_genre = request.POST.get('genre')
        new_location_coordinates = request.POST.get('location_coordinates')
        new_entry_fee = request.POST.get('entry_fee')
        new_opening_hours_week = request.POST.get('opening_hours_week')
        new_opening_hours_weekend = request.POST.get('opening_hours_weekend')
        new_covid_test_required = request.POST.get('covid_test_required')
        new_underage_visitors_allowed = request.POST.get('underage_visitors_allowed')
        if new_covid_test_required is None:
            new_covid_test_required = False
        if new_underage_visitors_allowed is None:
            new_underage_visitors_allowed = False
        if 'picture' in request.FILES:
            new_picture = request.FILES['picture']
        else:
            new_picture = Club.default
        club = Club.objects.get_or_create(name=new_club_name,
                                          club_description=new_club_description,
                                          city=new_city,
                                          website_url=new_website_url,
                                          genre=new_genre,
                                          location_coordinates=new_location_coordinates,
                                          entry_fee=new_entry_fee,
                                          opening_hours_week=new_opening_hours_week,
                                          opening_hours_weekend=new_opening_hours_weekend,
                                          picture=new_picture,
                                          covid_test_required=new_covid_test_required,
                                          underage_visitors_allowed=new_underage_visitors_allowed,
                                          average_rating=0.0,
                                          user_reported_safety=True)[0]
        club.save()
        user = request.user
        clubmate_user = UserProfile.objects.get_or_create(user=user)[0]
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


# @login_required
# def edit_picture(request, username):
#     if  request.method == 'POST':
#         user = request.user
#         clubmate_user=UserProfile.objects.get_or_create(user=user)[0]
#         new_picture = request.FILES.get('picture')
#         clubmate_user.picture = new_picture
#         clubmate_user.save()
#         return redirect((reverse('clubmate:profile', kwargs={'username': user.username})))
#     else:
#         context_dict = {'clubmate_user': clubmate_user}
#         return render(request, 'clubmate/edit_picture.html', context_dict)


@login_required
def edit_picture(request, username):
    context_dict = {}
    if request.method == 'POST':
        user = request.user
        clubmate_user = UserProfile.objects.get(user=user)
        if 'picture' in request.FILES:
            new_picture = request.FILES['picture']
        else:
            new_picture = UserProfile.default
        clubmate_user.picture = new_picture
        clubmate_user.save()
        context_dict['clubmate_user'] = clubmate_user
        return redirect((reverse('clubmate:profile', kwargs={'username': user.username})))
    else:
        permissions_check_clubmate_user(request, context_dict)
        return render(request, 'clubmate/edit_picture.html', context_dict)


@login_required  # Restrict to club owner
def edit_club(request, club_id):
    club = Club.objects.get(id=club_id)
    context_dict = {'club_id': club_id, 'club': club}
    permissions_check_clubmate_user(request, context_dict)
    if request.method == 'POST':
        new_club_name = request.POST.get('name')
        new_club_description = request.POST.get('club_description')
        new_city = request.POST.get('city')
        new_website_url = request.POST.get('website_url')
        new_genre = request.POST.get('genre')
        new_location_coordinates = request.POST.get('location_coordinates')
        new_entry_fee = request.POST.get('entry_fee')
        new_opening_hours_week = request.POST.get('opening_hours_week')
        new_opening_hours_weekend = request.POST.get('opening_hours_weekend')
        new_covid_test_required = request.POST.get('covid_test_required')
        new_underage_visitors_allowed = request.POST.get('underage_visitors_allowed')
        if new_covid_test_required is None:
            new_covid_test_required = False
        if new_underage_visitors_allowed is None:
            new_underage_visitors_allowed = False
        if 'picture' in request.FILES:
            new_picture = request.FILES['picture']
        else:
            new_picture = Club.default
        club.name = new_club_name
        club.club_description = new_club_description
        club.city = new_city
        club.website_url = new_website_url
        club.genre = new_genre
        club.location_coordinates = new_location_coordinates
        club.entry_fee = new_entry_fee
        club.opening_hours_week = new_opening_hours_week
        club.opening_hours_weekend = new_opening_hours_weekend
        club.picture = new_picture
        club.covid_test_required = new_covid_test_required
        club.underage_visitors_allowed = new_underage_visitors_allowed
        club.save()

        return render(request, 'clubmate/operation_successful.html')
    else:
        return render(request, 'clubmate/edit_club.html', context=context_dict)


@login_required  # Restrict to club owner
def delete_club(request, club_id):
    user = request.user
    club = Club.objects.get(id=club_id)
    club.delete()
    return redirect(reverse('clubmate:profile', kwargs={'username': user.username}))


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
