from django.urls import path

from clubmate import views

app_name = 'clubmate'

urlpatterns = [
    path('', views.index, name='index'),
]
