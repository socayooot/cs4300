# cs4300
In this repository, you will find all my work during the course of Fall 2026, taking CS4300

## Setup

    python3 -m venv homework1_env --system-site-packages
    source homework1_env/bin/activate
    pip install -r Homework_1/requirements.txt

## Running the code

    python3 Homework_1/src/Task1.py

## Running the tests

    cd Homework_1
    pytest -v

## use of ai

    All logic was originally written by me. I plugged in my original code and functionality into pardot which it stated that I did not fulfill
    the requirements. I then used Claude to fix and modify the code so that it is formatted in the correct way for grading. You will also be able
    to see that it is my code by looking at commits: 2899a6c. The changes that ai made was, converting my test scripts to pytest tests, refactor my 
    functions so that it no longer uses the input() command. In Task4, I also had ai remove the explicit type check and added a gitignore and     requirements.txt

## Homework 2: Movie Theater Booking (Django)

Live site (Render): https://movie-theater-bookings.onrender.com

Note: this runs on Render's free tier, so the first page load after a quiet period can take up to a minute while the server wakes up. The free tier also uses a temporary SQLite database, so accounts and bookings are reset whenever the service restarts or redeploys. Sample movies and seats are re-added on every deploy.

### What it does

A movie theater booking app built with Django and Django REST Framework. Users can view movies, book seats, and see their booking history, both through a Bootstrap web interface and through a REST API. The web pages and the API use the same booking logic (bookings/services.py), so they always show the same data and a seat can never be double-booked.

Seats are shared across all movies, as the assignment's Seat model specifies, so a booked seat is unavailable for every movie. A per-showing seat model would be the next improvement.

### Project structure

    Homework_2/
        requirements.txt
        movie_theater_booking/
            manage.py
            build.sh                      build steps used by Render
            .coveragerc                   coverage settings
            movie_theater_booking/        project settings and root urls
            bookings/                     the app
                models.py                 Movie, Seat, Booking
                services.py               book_seat() shared booking logic
                serializers.py            JSON serializers
                views.py                  DRF viewsets and the template views
                urls.py                   API routes (/api/...)
                page_urls.py              web page routes
                templates/bookings/       base, movie_list, seat_booking, booking_history
                templates/registration/   login, register
                management/commands/      seed (adds sample movies and seats)
                tests.py                  unit and integration tests
            features/                     Behave (BDD) scenarios and steps

### Setup

    python3 -m venv homework2_env --system-site-packages
    source homework2_env/bin/activate
    pip install -r Homework_2/requirements.txt
    cd Homework_2/movie_theater_booking
    python manage.py migrate
    python manage.py seed
    python manage.py createsuperuser

### Running the app

    export DEBUG=True        (local development only; Render keeps it off)
    python manage.py runserver 0.0.0.0:3000

In DevEdu, open it with the "app" button. Pages: / (movies), /history/ (my bookings), /register/, /login/, /admin/.

### API endpoints

    /api/movies/                  list movies (public); create/edit/delete is staff-only
    /api/seats/                   read-only: list seats (?available=true) and seat availability
    /api/seats/<id>/book/         POST {"movie": <id>} to book a seat (login required)
    /api/bookings/                POST to book a seat, GET my booking history, DELETE to cancel (bookings can't be  edited)

### Running the tests

    python manage.py test                    unit and API integration tests
    coverage run manage.py test              measure coverage
    coverage report -m
    python manage.py behave                  Behave (BDD) scenarios

### Deployment (Render)

    Root directory:  Homework_2/movie_theater_booking
    Build command:   bash build.sh
    Start command:   gunicorn movie_theater_booking.wsgi:application
    Environment:     SECRET_KEY, DEBUG=False, PYTHON_VERSION=3.12.3,
                     DJANGO_SUPERUSER_USERNAME, DJANGO_SUPERUSER_PASSWORD,
                     DJANGO_SUPERUSER_EMAIL

### Homework 2: use of ai

    I used Claude (Anthropic) throughout this assignment as a step-by-step guide.
    Claude wrote the first versions of: the models, services.py, serializers,
    viewsets and URL routing, the Bootstrap templates, the unit/integration
    tests in tests.py, the Behave feature and step files, the seed command,
    build.sh, and the settings changes for Render (whitenoise, gunicorn,
    environment variables). I typed or pasted the code into DevEdu, ran every
    command, fixed my own mistakes (for example a misplaced INSTALLED_APPS
    entry, a mistyped environment variable name on Render, and a committed
    db.sqlite3), tested the pages and API by hand, and deployed to Render.
    My commit messages show the order I did things in. 

    Additionally, I worked with Pardot, after feedback, I used Claude to help me 
    close a gap where PATCH on a booking could take a booked seat. Bookings can no 
    longer be edited, seats are read-only through the API, and movie writes are 
    staff-only. I added tests for each case."
