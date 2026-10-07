"""Unit and integration tests for the bookings app.

Run with:  python manage.py test
Layout:
  * Model tests          - the models behave and print nicely
  * Service tests        - book_seat() business logic
  * API integration tests - status codes and JSON shape for /api/...
  * Web page tests       - the Bootstrap pages built with Django templates
"""
from datetime import date

from django.contrib.auth.models import User
from django.db import IntegrityError, transaction
from django.test import TestCase
from rest_framework.test import APITestCase

from .models import Booking, Movie, Seat
from .services import SeatUnavailable, book_seat


def make_movie(title="The Matrix"):
    """Helper: create a movie with sensible defaults."""
    return Movie.objects.create(
        title=title,
        description="A hacker learns the truth.",
        release_date=date(1999, 3, 31),
        duration=136,
    )


# --------------------------------------------------------------------------
# Models
# --------------------------------------------------------------------------
class ModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("alice", password="pw12345!")
        self.movie = make_movie()
        self.seat = Seat.objects.create(seat_number="A1")

    def test_movie_str_is_title(self):
        self.assertEqual(str(self.movie), "The Matrix")

    def test_seat_str_is_seat_number(self):
        self.assertEqual(str(self.seat), "A1")

    def test_seat_defaults_to_available(self):
        self.assertFalse(self.seat.booking_status)

    def test_seat_numbers_must_be_unique(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Seat.objects.create(seat_number="A1")

    def test_booking_str_and_auto_date(self):
        booking = Booking.objects.create(movie=self.movie, seat=self.seat, user=self.user)
        self.assertEqual(str(booking), "alice - The Matrix - seat A1")
        self.assertIsNotNone(booking.booking_date)

    def test_movies_are_ordered_by_title(self):
        make_movie("Alien")
        titles = list(Movie.objects.values_list("title", flat=True))
        self.assertEqual(titles, ["Alien", "The Matrix"])


# --------------------------------------------------------------------------
# Service layer
# --------------------------------------------------------------------------
class BookSeatServiceTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("alice", password="pw12345!")
        self.movie = make_movie()
        self.seat = Seat.objects.create(seat_number="A1")

    def test_book_seat_creates_booking_and_marks_seat(self):
        booking = book_seat(self.user, self.movie, self.seat)
        self.seat.refresh_from_db()
        self.assertTrue(self.seat.booking_status)
        self.assertEqual(booking.user, self.user)
        self.assertEqual(booking.movie, self.movie)

    def test_book_seat_twice_raises(self):
        book_seat(self.user, self.movie, self.seat)
        with self.assertRaises(SeatUnavailable):
            book_seat(self.user, self.movie, self.seat)
        self.assertEqual(Booking.objects.count(), 1)


# --------------------------------------------------------------------------
# REST API integration tests
# --------------------------------------------------------------------------
class MovieApiTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user("alice", password="pw12345!")
        self.movie = make_movie()

    def test_list_is_public_and_has_expected_fields(self):
        response = self.client.get("/api/movies/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(
            set(response.json()[0]),
            {"id", "title", "description", "release_date", "duration"},
        )

    def test_retrieve_one_movie(self):
        response = self.client.get(f"/api/movies/{self.movie.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["title"], "The Matrix")

    def test_retrieve_missing_movie_is_404(self):
        self.assertEqual(self.client.get("/api/movies/9999/").status_code, 404)

    def test_create_requires_login(self):
        response = self.client.post("/api/movies/", {"title": "X"})
        self.assertIn(response.status_code, (401, 403))

    def test_create_update_delete_when_logged_in(self):
        self.client.force_authenticate(self.user)
        payload = {
            "title": "Inception",
            "description": "Dreams.",
            "release_date": "2010-07-16",
            "duration": 148,
        }
        created = self.client.post("/api/movies/", payload)
        self.assertEqual(created.status_code, 201)
        movie_id = created.json()["id"]

        updated = self.client.patch(f"/api/movies/{movie_id}/", {"duration": 150})
        self.assertEqual(updated.status_code, 200)
        self.assertEqual(updated.json()["duration"], 150)

        deleted = self.client.delete(f"/api/movies/{movie_id}/")
        self.assertEqual(deleted.status_code, 204)
        self.assertFalse(Movie.objects.filter(pk=movie_id).exists())

    def test_create_with_missing_fields_is_400(self):
        self.client.force_authenticate(self.user)
        response = self.client.post("/api/movies/", {"title": "No date"})
        self.assertEqual(response.status_code, 400)


class SeatApiTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user("alice", password="pw12345!")
        self.movie = make_movie()
        self.free = Seat.objects.create(seat_number="A1")
        self.taken = Seat.objects.create(seat_number="A2", booking_status=True)

    def test_list_shows_all_seats(self):
        response = self.client.get("/api/seats/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)

    def test_available_filter_only_returns_free_seats(self):
        response = self.client.get("/api/seats/?available=true")
        numbers = [seat["seat_number"] for seat in response.json()]
        self.assertEqual(numbers, ["A1"])

    def test_book_action_requires_login(self):
        response = self.client.post(f"/api/seats/{self.free.id}/book/", {"movie": self.movie.id})
        self.assertIn(response.status_code, (401, 403))

    def test_book_action_books_the_seat(self):
        self.client.force_authenticate(self.user)
        response = self.client.post(f"/api/seats/{self.free.id}/book/", {"movie": self.movie.id})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["user"], "alice")
        self.free.refresh_from_db()
        self.assertTrue(self.free.booking_status)

    def test_book_action_on_taken_seat_is_400(self):
        self.client.force_authenticate(self.user)
        response = self.client.post(f"/api/seats/{self.taken.id}/book/", {"movie": self.movie.id})
        self.assertEqual(response.status_code, 400)
        self.assertIn("already booked", response.json()["detail"])

    def test_book_action_with_unknown_movie_is_404(self):
        self.client.force_authenticate(self.user)
        response = self.client.post(f"/api/seats/{self.free.id}/book/", {"movie": 9999})
        self.assertEqual(response.status_code, 404)


class BookingApiTests(APITestCase):
    def setUp(self):
        self.alice = User.objects.create_user("alice", password="pw12345!")
        self.bob = User.objects.create_user("bob", password="pw12345!")
        self.movie = make_movie()
        self.seat1 = Seat.objects.create(seat_number="A1")
        self.seat2 = Seat.objects.create(seat_number="A2")

    def test_list_requires_login(self):
        self.assertIn(self.client.get("/api/bookings/").status_code, (401, 403))

    def test_create_booking_marks_seat_booked(self):
        self.client.force_authenticate(self.alice)
        response = self.client.post(
            "/api/bookings/", {"movie": self.movie.id, "seat": self.seat1.id}
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            set(response.json()), {"id", "movie", "seat", "user", "booking_date"}
        )
        self.seat1.refresh_from_db()
        self.assertTrue(self.seat1.booking_status)

    def test_cannot_double_book_a_seat(self):
        self.client.force_authenticate(self.alice)
        data = {"movie": self.movie.id, "seat": self.seat1.id}
        self.assertEqual(self.client.post("/api/bookings/", data).status_code, 201)
        second = self.client.post("/api/bookings/", data)
        self.assertEqual(second.status_code, 400)
        self.assertEqual(Booking.objects.count(), 1)

    def test_booking_with_invalid_seat_is_400(self):
        self.client.force_authenticate(self.alice)
        response = self.client.post("/api/bookings/", {"movie": self.movie.id, "seat": 9999})
        self.assertEqual(response.status_code, 400)

    def test_history_only_contains_own_bookings(self):
        Booking.objects.create(movie=self.movie, seat=self.seat1, user=self.alice)
        Booking.objects.create(movie=self.movie, seat=self.seat2, user=self.bob)
        self.client.force_authenticate(self.alice)
        data = self.client.get("/api/bookings/").json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["user"], "alice")

    def test_cannot_see_someone_elses_booking(self):
        other = Booking.objects.create(movie=self.movie, seat=self.seat2, user=self.bob)
        self.client.force_authenticate(self.alice)
        self.assertEqual(self.client.get(f"/api/bookings/{other.id}/").status_code, 404)

    def test_cancelling_a_booking_frees_the_seat(self):
        self.client.force_authenticate(self.alice)
        self.client.post("/api/bookings/", {"movie": self.movie.id, "seat": self.seat1.id})
        booking = Booking.objects.get()
        response = self.client.delete(f"/api/bookings/{booking.id}/")
        self.assertEqual(response.status_code, 204)
        self.seat1.refresh_from_db()
        self.assertFalse(self.seat1.booking_status)
        self.assertEqual(Booking.objects.count(), 0)


# --------------------------------------------------------------------------
# Web pages (Django templates)
# --------------------------------------------------------------------------
class WebPageTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("carol", password="pw12345!")
        self.movie = make_movie()
        self.seat = Seat.objects.create(seat_number="B2")
        self.booking_url = f"/movies/{self.movie.id}/book/"

    def login(self):
        self.client.login(username="carol", password="pw12345!")

    def test_movie_list_is_public_and_shows_movies(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "The Matrix")
        self.assertContains(response, "Book Now")

    def test_movie_list_with_no_movies_shows_message(self):
        Movie.objects.all().delete()
        self.assertContains(self.client.get("/"), "No movies yet")

    def test_booking_page_requires_login(self):
        response = self.client.get(self.booking_url)
        self.assertRedirects(
            response, f"/login/?next={self.booking_url}", fetch_redirect_response=False
        )

    def test_booking_page_lists_seats(self):
        self.login()
        response = self.client.get(self.booking_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "B2")

    def test_booking_page_for_missing_movie_is_404(self):
        self.login()
        self.assertEqual(self.client.get("/movies/9999/book/").status_code, 404)

    def test_booking_a_seat_through_the_page(self):
        self.login()
        response = self.client.post(self.booking_url, {"seat": self.seat.id})
        self.assertRedirects(response, "/history/")
        self.seat.refresh_from_db()
        self.assertTrue(self.seat.booking_status)
        self.assertEqual(Booking.objects.filter(user=self.user).count(), 1)

    def test_booking_a_taken_seat_shows_error_and_does_not_double_book(self):
        self.login()
        self.client.post(self.booking_url, {"seat": self.seat.id})
        response = self.client.post(self.booking_url, {"seat": self.seat.id}, follow=True)
        self.assertContains(response, "already booked")
        self.assertEqual(Booking.objects.count(), 1)

    def test_booking_with_unknown_seat_is_404(self):
        self.login()
        self.assertEqual(self.client.post(self.booking_url, {"seat": 9999}).status_code, 404)

    def test_history_requires_login(self):
        response = self.client.get("/history/")
        self.assertRedirects(response, "/login/?next=/history/", fetch_redirect_response=False)

    def test_history_lists_only_my_bookings(self):
        other = User.objects.create_user("dave", password="pw12345!")
        other_seat = Seat.objects.create(seat_number="C3")
        Booking.objects.create(movie=self.movie, seat=self.seat, user=self.user)
        Booking.objects.create(movie=self.movie, seat=other_seat, user=other)
        self.login()
        response = self.client.get("/history/")
        self.assertContains(response, "B2")
        self.assertNotContains(response, "C3")

    def test_history_empty_state(self):
        self.login()
        self.assertContains(self.client.get("/history/"), "no bookings yet")

    def test_login_page_renders(self):
        self.assertEqual(self.client.get("/login/").status_code, 200)

    def test_login_redirects_to_movie_list(self):
        response = self.client.post("/login/", {"username": "carol", "password": "pw12345!"})
        self.assertRedirects(response, "/")

    def test_register_creates_account_and_logs_in(self):
        response = self.client.post(
            "/register/",
            {"username": "newuser", "password1": "Str0ng-pass-99", "password2": "Str0ng-pass-99"},
        )
        self.assertRedirects(response, "/")
        self.assertTrue(User.objects.filter(username="newuser").exists())
        self.assertContains(self.client.get("/"), "Log out (newuser)")

    def test_register_with_mismatched_passwords_fails(self):
        response = self.client.post(
            "/register/",
            {"username": "newuser", "password1": "Str0ng-pass-99", "password2": "different"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username="newuser").exists())

    def test_register_page_renders(self):
        self.assertEqual(self.client.get("/register/").status_code, 200)

    def test_logout_ends_the_session(self):
        self.login()
        response = self.client.post("/logout/")
        self.assertRedirects(response, "/", fetch_redirect_response=False)
        self.assertContains(self.client.get("/"), "Log in")

# --------------------------------------------------------------------------
# Management command used by the Render build
# --------------------------------------------------------------------------
class SeedCommandTests(TestCase):
    def test_seed_adds_sample_data_and_is_safe_to_repeat(self):
        from io import StringIO

        from django.core.management import call_command

        call_command("seed", stdout=StringIO())
        call_command("seed", stdout=StringIO())  # running twice must not duplicate
        self.assertEqual(Movie.objects.count(), 3)
        self.assertEqual(Seat.objects.count(), 24)
