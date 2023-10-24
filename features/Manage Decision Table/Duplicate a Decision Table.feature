Feature: Duplicate a Decision Table

  Scenario: User successfully duplicates a decision table
    Given the user is on the decision tables management page
    And there is an existing decision table named "OriginalDecisionTable"
    When the user selects to duplicate the decision table named "OriginalDecisionTable"
    Then the system should create a duplicate of "OriginalDecisionTable"
    And the user should see a success message

  Scenario: User tries to duplicate a non-existent decision table
    Given the user is on the decision tables management page
    And there is no decision table named "NonExistentTable"
    When the user selects to duplicate the decision table named "NonExistentTable"
    Then the system should display an error message

  Scenario: User duplicates a decision table with an invalid name
    Given the user is on the decision tables management page
    And there is an existing decision table named "ExistingTable"
    When the user selects to duplicate the decision table named "ExistingTable"
    And the user enters an invalid name for the duplicate (e.g., empty or containing special characters)
    Then the system should not create the duplicate decision table
    And the user should see an error message about the invalid name

  Scenario: User cancels duplicating a decision table
    Given the user is on the decision tables management page
    And there is an existing decision table named "DecisionTableToCancel"
    When the user selects to duplicate the decision table named "DecisionTableToCancel"
    And the user cancels the duplication
    Then the system should not create the duplicate decision table
    And the user should see a cancellation message
