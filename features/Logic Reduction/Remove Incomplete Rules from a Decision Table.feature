Feature: Remove Incomplete Rules from a Decision Table

  Scenario: User successfully removes incomplete rules from a decision table
    Given the user is on the decision table editing page for "DecisionTable"
    And "DecisionTable" has existing rules, some of which are incomplete
    When the user selects to remove incomplete rules
    And the user confirms the removal
    Then the system should remove the incomplete rules from "DecisionTable"
    And the user should see a success message

  Scenario: User tries to remove incomplete rules from a decision table with no incomplete rules
    Given the user is on the decision table editing page for "DecisionTableNoIncompleteRules"
    And "DecisionTableNoIncompleteRules" has existing rules that are all complete
    When the user selects to remove incomplete rules
    Then the system should indicate that there are no incomplete rules in "DecisionTableNoIncompleteRules"

  Scenario: User cancels removing incomplete rules
    Given the user is on the decision table editing page for "DecisionTableToCancel"
    And "DecisionTableToCancel" has existing rules, some of which are incomplete
    When the user selects to remove incomplete rules
    And the user cancels the removal
    Then the system should not remove any incomplete rules
    And the user should see a cancellation message
