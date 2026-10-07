from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Booking, Movie, Seat
from .serializers import BookingSerializer, MovieSerializer, SeatSerializer
from .services import SeatUnavailable, book_seat


class MovieViewSet(viewsets.ModelViewSet):
    """Full CRUD for movies. Anyone can read; writing requires login."""
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


class SeatViewSet(viewsets.ModelViewSet):
    """Seat availability, plus a `book` action.

    GET  /api/seats/?available=true   -> only unbooked seats
    POST /api/seats/<id>/book/        -> body: {"movie": <movie id>}
    """
    queryset = Seat.objects.all()
    serializer_class = SeatSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.query_params.get("available") == "true":
            queryset = queryset.filter(booking_status=False)
        return queryset

    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated])
    def book(self, request, pk=None):
        seat = self.get_object()
        movie = get_object_or_404(Movie, pk=request.data.get("movie"))
        try:
            booking = book_seat(request.user, movie, seat)
        except SeatUnavailable as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(BookingSerializer(booking).data, status=status.HTTP_201_CREATED)


class BookingViewSet(viewsets.ModelViewSet):
    """Users book seats (POST) and see their own booking history (GET)."""
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Each user only ever sees their own bookings.
        return Booking.objects.filter(user=self.request.user).select_related("movie", "seat")

    def perform_destroy(self, instance):
        # Cancelling a booking frees the seat again.
        seat = instance.seat
        instance.delete()
        seat.booking_status = False
        seat.save(update_fields=["booking_status"])

# ---------------- Template (web page) views ----------------
# These use the same book_seat() function as the API, so the pages and the
# API always show and change the same data.

def movie_list(request):
    """Page 1: list every movie with a Book Now button."""
    return render(request, "bookings/movie_list.html", {"movies": Movie.objects.all()})


@login_required
def seat_booking(request, movie_id):
    """Page 2: pick a seat for one movie (GET shows seats, POST books one)."""
    movie = get_object_or_404(Movie, pk=movie_id)
    if request.method == "POST":
        seat = get_object_or_404(Seat, pk=request.POST.get("seat"))
        try:
            book_seat(request.user, movie, seat)
        except SeatUnavailable as exc:
            messages.error(request, str(exc))
            return redirect("book_seat", movie_id=movie.id)
        messages.success(request, f"Booked seat {seat.seat_number} for {movie.title}!")
        return redirect("booking_history")
    return render(request, "bookings/seat_booking.html",
                  {"movie": movie, "seats": Seat.objects.all()})


@login_required
def booking_history(request):
    """Page 3: the logged-in user's bookings."""
    bookings = Booking.objects.filter(user=request.user).select_related("movie", "seat")
    return render(request, "bookings/booking_history.html", {"bookings": bookings})


def register(request):
    """Sign-up page: create an account and log in right away."""
    form = UserCreationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        login(request, form.save())
        return redirect("movie_list")
    return render(request, "registration/register.html", {"form": form})