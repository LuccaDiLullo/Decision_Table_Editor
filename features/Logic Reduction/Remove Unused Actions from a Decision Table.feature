Feature: Remove Unused Actions from a Decision Table

  Scenario: User successfully removes unused actions from a decision table
    Given the user is on the decision table editing page for "DecisionTable"
    And "DecisionTable" has existing actions, some of which are unused in rules
    When the user selects to remove unused actions
    And the user confirms the removal
    Then the system should remove the unused actions from "DecisionTable"
    And the user should see a success message

  Scenario: User tries to remove unused actions from a decision table with no unused actions
    Given the user is on the decision table editing page for "DecisionTableNoUnusedActions"
    And "DecisionTableNoUnusedActions" has existing actions that are all used in rules
    When the user selects to remove unused actions
    Then the system should indicate that there are no unused actions in "DecisionTableNoUnusedActions"

  Scenario: User cancels removing unused actions
    Given the user is on the decision table editing page for "DecisionTableToCancel"
    And "DecisionTableToCancel" has existing actions, some of which are unused in rules
    When the user selects to remove unused actions
    And the user cancels the removal
    Then the system should not remove any unused actions
    And the user should see a cancellation message
