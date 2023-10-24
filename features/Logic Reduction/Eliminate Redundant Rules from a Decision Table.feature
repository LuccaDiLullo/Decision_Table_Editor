Feature: Eliminate Redundant Rules from a Decision Table

  Scenario: User successfully eliminates redundant rules from a decision table
    Given the user is on the decision table editing page for "DecisionTable"
    And "DecisionTable" has existing rules, some of which are redundant
    When the user selects to eliminate redundant rules
    And the user confirms the elimination
    Then the system should eliminate the redundant rules from "DecisionTable"
    And the user should see a success message

  Scenario: User tries to eliminate redundant rules from a decision table with no redundant rules
    Given the user is on the decision table editing page for "DecisionTableNoRedundantRules"
    And "DecisionTableNoRedundantRules" has existing rules with no redundancies
    When the user selects to eliminate redundant rules
    Then the system should indicate that there are no redundant rules in "DecisionTableNoRedundantRules"

  Scenario: User cancels eliminating redundant rules
    Given the user is on the decision table editing page for "DecisionTableToCancel"
    And "DecisionTableToCancel" has existing rules, some of which are redundant
    When the user selects to eliminate redundant rules
    And the user cancels the elimination
    Then the system should not eliminate any redundant rules
    And the user should see a cancellation message
