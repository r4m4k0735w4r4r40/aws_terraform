Feature: Booking API
  Scenario: checking sign up
    Given interface arn 'signup_lambda'
    When given user data 'test' 'passwd' 'test@gmail.com'
    Then the signup response is 200

  Scenario: checking login
    Given interface arn 'signin_lambda'
    When given login data 'test' 'passwd'
    Then the signin response is 200

  Scenario: booking ticket
    Given interface arn 'booking_lambda'
    When given booking data '1001' '07:00' '28-07-2022'
    Then the booking response is 200

  Scenario: booking history
    Given interface arn 'booking_his_lambda'
    When requested for history
    Then the history response is 200