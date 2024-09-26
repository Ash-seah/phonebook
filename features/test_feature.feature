Feature: FastAPI endpoints testing

  Scenario: Get all records
    Given the FastAPI server is running
    When I send a GET request to "/"
    Then I should receive a list of all records

  Scenario: Add a new record
    Given the FastAPI server is running
    When I send a PUT request to "/" with name "John" and number "12345" and email "john@gmail.com"
    Then the record should be added to the database

  Scenario: Query by name
    Given the FastAPI server is running
    When I send a GET request to "/query/name/" with name "John"
    Then I should receive the records matching the name "John"
