from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path("", views.movie_list, name="movie_list"),
    path("movies/<int:movie_id>/book/", views.seat_booking, name="book_seat"),
    path("history/", views.booking_history, name="booking_history"),
    path("register/", views.register, name="register"),
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
]