Feature: Utilize Algorithms from E2GRULEWRITER to Optimize Decision Tables

  Scenario: User successfully optimizes a decision table using E2GRULEWRITER algorithms
    Given the user is on the decision table editing page for "DecisionTable"
    And "DecisionTable" has existing rules
    When the user selects to optimize the decision table using E2GRULEWRITER algorithms
    And the user specifies optimization settings (if applicable)
    And the user applies the optimization
    Then the system should optimize "DecisionTable" using E2GRULEWRITER algorithms
    And the user should see a success message

  Scenario: User tries to optimize a decision table with no existing rules
    Given the user is on the decision table editing page for "EmptyDecisionTable"
    And "EmptyDecisionTable" does not have any rules
    When the user selects to optimize the decision table using E2GRULEWRITER algorithms
    Then the system should indicate that there are no rules to optimize in the empty table

  Scenario: User cancels the optimization process
    Given the user is on the decision table editing page for "DecisionTableToCancel"
    And "DecisionTableToCancel" has existing rules
    When the user selects to optimize the decision table using E2GRULEWRITER algorithms
    And the user cancels the optimization process
    Then the system should not perform any optimization
    And the user should see a cancellation message
