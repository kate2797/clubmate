from django.urls import path

from clubmate import views

app_name = 'clubmate'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('discover/', views.discover, name='discover'),
    path('club_detail/<int:club_id>/', views.club_detail, name='club_detail'),
    path('ratings/', views.ratings, name='ratings'),
    path('rating_detail/<int:rating_id>/', views.rating_detail, name='rating_detail'),
    path('rate/<int:club_id>/', views.rate_detail, name='rate_detail'),  # New, to rate a specific club
    path('rate/', views.rate, name='rate'),
    path('add_club/', views.add_club, name='add_club'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('edit_club/<int:club_id>/', views.edit_club, name='edit_club'),
    path('delete_club/<int:club_id>/', views.delete_club, name='delete_club'),
    path('edit_rating/<int:rating_id>/', views.edit_rating, name='edit_rating'),
    path('delete_rating/<int:rating_id>/', views.delete_rating, name='delete_rating'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('upvote/<int:rating_id>/', views.upvote_rating, name='upvote_rating'),  # New, to upvote reviews
    path('save/<int:club_id>/', views.save_club, name='save_club'),  # New, to save club to a profile

    path('rate_content/<int:rating_id>/', views.rate_content, name='rate_content'),
]
