Feature: Create a Decision Table

  Scenario: User creates a new decision table
    Given the user is on the decision table creation page
    When the user selects to create a new decision table
    Then the system should provide a blank decision table template

  Scenario: User creates a decision table with a specific name
    Given the user is on the decision table creation page
    When the user enters the name "MyNewDecisionTable" for the decision table
    And the user selects to create the decision table
    Then the system should create a new decision table with the name "MyNewDecisionTable"

  Scenario: User cancels the creation of a new decision table
    Given the user is on the decision table creation page
    When the user selects to cancel the creation
    Then the system should not create a new decision table
    And the user should remain on the previous page