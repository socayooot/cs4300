#Both the API and the web pages call this one function, so they must stay in sync so that
#a customer will never double book a seat
from django.db import transaction

from .models import Booking, Seat


class SeatUnavailable(Exception):
    """Raised when someone tries to book a seat that is already taken."""


def book_seat(user, movie, seat):
    """Mark `seat` as booked and create a Booking for `user`."""
    with transaction.atomic():
        locked = Seat.objects.select_for_update().get(pk=seat.pk)
        if locked.booking_status:
            raise SeatUnavailable(f"Seat {locked.seat_number} is already booked.")
        locked.booking_status = True
        locked.save(update_fields=["booking_status"])
        return Booking.objects.create(movie=movie, seat=locked, user=user)