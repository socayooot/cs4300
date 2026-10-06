from django.shortcuts import get_object_or_404
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
