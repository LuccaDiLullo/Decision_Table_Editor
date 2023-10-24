Feature: Delete a Decision Table

  Scenario: User successfully deletes a decision table
    Given the user is on the decision tables management page
    And there is an existing decision table named "DecisionTableToDelete"
    When the user selects to delete the decision table
    Then the system should delete the decision table
    And the user should see a success message

  Scenario: User cancels decision table deletion
    Given the user is on the decision tables management page
    And there is an existing decision table named "DecisionTableNotToDelete"
    When the user selects to delete the decision table
    And the user cancels the deletion
    Then the system should not delete the decision table
    And the user should see a cancellation message

  Scenario: User tries to delete a non-existent decision table
    Given the user is on the decision tables management page
    And there is no decision table named "NonExistentTable"
    When the user selects to delete the decision table named "NonExistentTable"
    Then the system should display an error message

  Scenario: User deletes a decision table with associated rules
    Given the user is on the decision tables management page
    And there is an existing decision table named "TableWithRules"
    And "TableWithRules" has associated rules
    When the user selects to delete the decision table
    Then the system should prompt for confirmation
    When the user confirms the deletion
    Then the system should delete the decision table and its associated rules
    And the user should see a success message
