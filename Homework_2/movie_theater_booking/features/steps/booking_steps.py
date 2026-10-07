"""Step definitions: each plain-English line in booking.feature runs one of these."""
from datetime import date

from behave import given, then, when
from django.contrib.auth.models import User

from bookings.models import Booking, Movie, Seat

PASSWORD = "pw12345!"


# ------------------------------- Given -------------------------------
@given('the movie "{title}" exists')
def step_movie_exists(context, title):
    Movie.objects.create(
        title=title,
        description="A test movie.",
        release_date=date(1999, 3, 31),
        duration=136,
    )


@given('the seat "{number}" exists')
def step_seat_exists(context, number):
    Seat.objects.create(seat_number=number)


@given('a registered user "{username}" exists')
def step_user_exists(context, username):
    User.objects.create_user(username, password=PASSWORD)


@given('I am logged in as "{username}"')
def step_logged_in(context, username):
    context.client.login(username=username, password=PASSWORD)
    context.api.force_authenticate(User.objects.get(username=username))


@given('seat "{number}" was already booked by another user')
def step_seat_taken(context, number):
    other = User.objects.create_user("dave", password=PASSWORD)
    seat = Seat.objects.get(seat_number=number)
    seat.booking_status = True
    seat.save()
    Booking.objects.create(movie=Movie.objects.first(), seat=seat, user=other)


# ------------------------------- When --------------------------------
@when("I visit the movie list page")
def step_visit_movie_list(context):
    context.response = context.client.get("/")


@when('I book seat "{number}" for "{title}"')
def step_book_seat(context, number, title):
    movie = Movie.objects.get(title=title)
    seat = Seat.objects.get(seat_number=number)
    context.response = context.client.post(
        f"/movies/{movie.id}/book/", {"seat": seat.id}, follow=True
    )


@when('I visit the booking page for "{title}" without logging in')
def step_visit_booking_logged_out(context, title):
    movie = Movie.objects.get(title=title)
    context.response = context.client.get(f"/movies/{movie.id}/book/")


@when('I book seat "{number}" for "{title}" through the API')
def step_book_via_api(context, number, title):
    movie = Movie.objects.get(title=title)
    seat = Seat.objects.get(seat_number=number)
    context.api_response = context.api.post(
        "/api/bookings/", {"movie": movie.id, "seat": seat.id}
    )


# ------------------------------- Then --------------------------------
@then('I should see "{text}"')
def step_should_see(context, text):
    assert text in context.response.content.decode(), f"{text!r} not on the page"


@then('I should see the message "{text}"')
def step_should_see_message(context, text):
    assert text in context.response.content.decode(), f"{text!r} not on the page"


@then('seat "{number}" should be marked as booked')
def step_seat_marked_booked(context, number):
    assert Seat.objects.get(seat_number=number).booking_status is True


@then('my booking history page should show "{title}" and seat "{number}"')
def step_history_shows(context, title, number):
    page = context.client.get("/history/").content.decode()
    assert title in page and number in page, "booking missing from history page"


@then("I should have {count:d} bookings")
def step_booking_count(context, count):
    assert Booking.objects.filter(user__username="carol").count() == count


@then("I should be sent to the login page")
def step_redirected_to_login(context):
    assert context.response.status_code == 302
    assert context.response["Location"].startswith("/login/")


@then("the API response status should be {status:d}")
def step_api_status(context, status):
    assert context.api_response.status_code == status, context.api_response.status_code


@then("my API booking history should contain {count:d} booking")
def step_api_history(context, count):
    assert len(context.api.get("/api/bookings/").json()) == count
