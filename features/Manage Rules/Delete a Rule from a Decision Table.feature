Feature: Delete a Rule from a Decision Table

  Scenario: User successfully deletes an existing rule from a decision table
    Given the user is on the decision table editing page
    And there is an existing decision table named "DecisionTable"
    And "DecisionTable" has an existing rule
    When the user selects to delete a rule from "DecisionTable"
    And the user confirms the deletion
    Then the system should delete the rule from "DecisionTable"
    And the user should see a success message

  Scenario: User tries to delete a rule from a non-existent decision table
    Given the user is on the decision table editing page
    And there is no decision table named "NonExistentTable"
    When the user selects to delete a rule from "NonExistentTable"
    Then the system should display an error message

  Scenario: User tries to delete a rule from an empty decision table
    Given the user is on the decision table editing page
    And there is an existing decision table named "EmptyDecisionTable"
    When the user selects to delete a rule from "EmptyDecisionTable"
    Then the system should not delete any rule
    And the user should see an error message about the empty table

  Scenario: User cancels deleting a rule from a decision table
    Given the user is on the decision table editing page
    And there is an existing decision table named "DecisionTableToCancel"
    And "DecisionTableToCancel" has an existing rule
    When the user selects to delete a rule from "DecisionTableToCancel"
    And the user cancels the deletion
    Then the system should not delete the rule
    And the user should see a cancellation message
