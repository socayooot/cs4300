from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import BookingViewSet, MovieViewSet, SeatViewSet

# The router builds /movies/, /seats/ and /bookings/ (plus detail routes) for us.
router = DefaultRouter()
router.register("movies", MovieViewSet, basename="movie")
router.register("seats", SeatViewSet, basename="seat")
router.register("bookings", BookingViewSet, basename="booking")

urlpatterns = [
    path("", include(router.urls)),
]