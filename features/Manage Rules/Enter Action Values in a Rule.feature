Feature: Enter Action Values in a Rule

  Scenario: User successfully enters action values in a rule
    Given the user is on the rule editing page for "DecisionTable" and "Rule1"
    And there is an existing action named "Action1"
    And "DecisionTable" has an existing rule "Rule1"
    When the user enters specific action values for "Rule1"
    And the user saves the rule
    Then the system should update "Rule1" with the specified action values
    And the user should see a success message

  Scenario: User tries to enter action values in a rule for a non-existent action
    Given the user is on the rule editing page for "DecisionTable" and "Rule2"
    And there is no action named "NonExistentAction"
    And "DecisionTable" has an existing rule "Rule2"
    When the user tries to enter action values for "Rule2"
    Then the system should display an error message

  Scenario: User cancels entering action values in a rule
    Given the user is on the rule editing page for "DecisionTable" and "RuleToCancel"
    And there is an existing action named "ActionToCancel"
    And "DecisionTable" has an existing rule "RuleToCancel"
    When the user enters specific action values for "RuleToCancel"
    And the user cancels the entry
    Then the system should not update "RuleToCancel" with the entered values
    And the user should see a cancellation message
