Feature: Eliminate Irrelevant Conditions from a Decision Table

  Scenario: User successfully eliminates irrelevant conditions from a decision table
    Given the user is on the decision table editing page for "DecisionTable"
    And "DecisionTable" has existing conditions, some of which are irrelevant
    When the user selects to eliminate irrelevant conditions
    And the user confirms the elimination
    Then the system should remove the irrelevant conditions from "DecisionTable"
    And the user should see a success message

  Scenario: User tries to eliminate irrelevant conditions from a decision table with no irrelevant conditions
    Given the user is on the decision table editing page for "DecisionTableNoIrrelevantConditions"
    And "DecisionTableNoIrrelevantConditions" has existing conditions that are all relevant
    When the user selects to eliminate irrelevant conditions
    Then the system should indicate that there are no irrelevant conditions in "DecisionTableNoIrrelevantConditions"

  Scenario: User cancels eliminating irrelevant conditions
    Given the user is on the decision table editing page for "DecisionTableToCancel"
    And "DecisionTableToCancel" has existing conditions, some of which are irrelevant
    When the user selects to eliminate irrelevant conditions
    And the user cancels the elimination
    Then the system should not remove any irrelevant conditions
    And the user should see a cancellation message
