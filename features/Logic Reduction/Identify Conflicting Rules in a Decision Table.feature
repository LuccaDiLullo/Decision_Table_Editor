Feature: Identify Conflicting Rules in a Decision Table

  Scenario: User identifies conflicting rules in a decision table
    Given the user is on the decision table editing page for "DecisionTable"
    And "DecisionTable" has existing rules with conflicts
    When the user selects to identify conflicting rules
    Then the system should highlight or list the conflicting rules
    And the user should see a message indicating the presence of conflicts

  Scenario: User identifies conflicting rules in an empty decision table
    Given the user is on the decision table editing page for "EmptyDecisionTable"
    And "EmptyDecisionTable" does not have any rules
    When the user selects to identify conflicting rules
    Then the system should indicate that there are no conflicts in the empty table

  Scenario: User identifies conflicting rules in a decision table with no conflicts
    Given the user is on the decision table editing page for "DecisionTableNoConflicts"
    And "DecisionTableNoConflicts" has existing rules with no conflicts
    When the user selects to identify conflicting rules
    Then the system should indicate that there are no conflicts in "DecisionTableNoConflicts"

  Scenario: User cancels identifying conflicting rules
    Given the user is on the decision table editing page for "DecisionTableToCancel"
    And "DecisionTableToCancel" has existing rules with conflicts
    When the user selects to identify conflicting rules
    And the user cancels the identification process
    Then the system should not highlight or list the conflicting rules
    And the user should not see any message about conflicts
