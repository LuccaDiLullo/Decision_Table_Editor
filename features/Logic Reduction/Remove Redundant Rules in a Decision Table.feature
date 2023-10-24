Feature: Remove Redundant Rules in a Decision Table

  Scenario: User successfully removes redundant rules from a decision table
    Given the user is on the decision table editing page for "DecisionTable"
    And "DecisionTable" has existing rules, some of which are redundant
    When the user selects to remove redundant rules
    And the user confirms the removal
    Then the system should remove the redundant rules from "DecisionTable"
    And the user should see a success message

  Scenario: User tries to remove redundant rules from an empty decision table
    Given the user is on the decision table editing page for "EmptyDecisionTable"
    And "EmptyDecisionTable" does not have any rules
    When the user selects to remove redundant rules
    Then the system should indicate that there are no redundant rules in the empty table

  Scenario: User tries to remove redundant rules from a decision table with no redundancies
    Given the user is on the decision table editing page for "DecisionTableNoRedundancies"
    And "DecisionTableNoRedundancies" has existing rules with no redundancies
    When the user selects to remove redundant rules
    Then the system should indicate that there are no redundant rules in "DecisionTableNoRedundancies"

  Scenario: User cancels removing redundant rules
    Given the user is on the decision table editing page for "DecisionTableToCancel"
    And "DecisionTableToCancel" has existing rules, some of which are redundant
    When the user selects to remove redundant rules
    And the user cancels the removal
    Then the system should not remove any redundant rules
    And the user should see a cancellation message
