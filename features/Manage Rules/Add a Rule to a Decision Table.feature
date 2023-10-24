Feature: Add a Rule to a Decision Table

  Scenario: User successfully adds a new rule to a decision table
    Given the user is on the decision table editing page
    And there is an existing decision table named "DecisionTable"
    When the user selects to add a new rule to "DecisionTable"
    And the user specifies conditions and actions for the new rule
    And the user saves the new rule
    Then the system should add the new rule to "DecisionTable"
    And the user should see a success message

  Scenario: User tries to add a rule to a non-existent decision table
    Given the user is on the decision table editing page
    And there is no decision table named "NonExistentTable"
    When the user selects to add a new rule to "NonExistentTable"
    Then the system should display an error message

  Scenario: User cancels adding a new rule to a decision table
    Given the user is on the decision table editing page
    And there is an existing decision table named "DecisionTableToCancel"
    When the user selects to add a new rule to "DecisionTableToCancel"
    And the user cancels the addition
    Then the system should not add the new rule
    And the user should see a cancellation message
