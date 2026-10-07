Feature: Booking movie seats
  As a moviegoer
  I want to browse movies and book seats
  So that I have a seat for the show

  Background:
    Given the movie "The Matrix" exists
    And the seat "A1" exists
    And the seat "A2" exists
    And a registered user "carol" exists

  Scenario: Browsing the movie list
    When I visit the movie list page
    Then I should see "The Matrix"

  Scenario: Booking an available seat
    Given I am logged in as "carol"
    When I book seat "A1" for "The Matrix"
    Then seat "A1" should be marked as booked
    And my booking history page should show "The Matrix" and seat "A1"

  Scenario: Booking a seat that is already taken
    Given I am logged in as "carol"
    And seat "A1" was already booked by another user
    When I book seat "A1" for "The Matrix"
    Then I should see the message "already booked"
    And I should have 0 bookings

  Scenario: Booking requires a login
    When I visit the booking page for "The Matrix" without logging in
    Then I should be sent to the login page

  Scenario: Booking a seat through the API
    Given I am logged in as "carol"
    When I book seat "A2" for "The Matrix" through the API
    Then the API response status should be 201
    And my API booking history should contain 1 booking
