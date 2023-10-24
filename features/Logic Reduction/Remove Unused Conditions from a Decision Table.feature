Feature: Remove Unused Conditions from a Decision Table

  Scenario: User successfully removes unused conditions from a decision table
    Given the user is on the decision table editing page for "DecisionTable"
    And "DecisionTable" has existing conditions, some of which are unused in rules
    When the user selects to remove unused conditions
    And the user confirms the removal
    Then the system should remove the unused conditions from "DecisionTable"
    And the user should see a success message

  Scenario: User tries to remove unused conditions from a decision table with no unused conditions
    Given the user is on the decision table editing page for "DecisionTableNoUnusedConditions"
    And "DecisionTableNoUnusedConditions" has existing conditions that are all used in rules
    When the user selects to remove unused conditions
    Then the system should indicate that there are no unused conditions in "DecisionTableNoUnusedConditions"

  Scenario: User cancels removing unused conditions
    Given the user is on the decision table editing page for "DecisionTableToCancel"
    And "DecisionTableToCancel" has existing conditions, some of which are unused in rules
    When the user selects to remove unused conditions
    And the user cancels the removal
    Then the system should not remove any unused conditions
    And the user should see a cancellation message