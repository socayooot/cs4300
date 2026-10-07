from datetime import date

from django.core.management.base import BaseCommand

from bookings.models import Movie, Seat


class Command(BaseCommand):
    """Add sample movies and seats. Safe to run more than once."""

    help = "Add sample movies and seats."

    def handle(self, *args, **options):
        movies = [
            ("The Matrix", "A hacker learns the nature of reality.", date(1999, 3, 31), 136),
            ("Inception", "A thief enters people's dreams.", date(2010, 7, 16), 148),
            ("Spirited Away", "A girl wanders into a world of spirits.", date(2001, 7, 20), 125),
        ]
        for title, description, released, minutes in movies:
            Movie.objects.get_or_create(
                title=title,
                defaults={
                    "description": description,
                    "release_date": released,
                    "duration": minutes,
                },
            )
        for row in "ABCD":
            for number in range(1, 7):
                Seat.objects.get_or_create(seat_number=f"{row}{number}")
        self.stdout.write(self.style.SUCCESS("Seeded movies and seats."))
