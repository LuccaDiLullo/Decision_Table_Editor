Feature: Enter Condition Values in a Rule

  Scenario: User successfully enters condition values in a rule
    Given the user is on the rule editing page for "DecisionTable" and "Rule1"
    And there is an existing condition named "Condition1"
    And "DecisionTable" has an existing rule "Rule1"
    When the user enters specific condition values for "Rule1"
    And the user saves the rule
    Then the system should update "Rule1" with the specified condition values
    And the user should see a success message

  Scenario: User tries to enter condition values in a rule for a non-existent condition
    Given the user is on the rule editing page for "DecisionTable" and "Rule2"
    And there is no condition named "NonExistentCondition"
    And "DecisionTable" has an existing rule "Rule2"
    When the user tries to enter condition values for "Rule2"
    Then the system should display an error message

  Scenario: User cancels entering condition values in a rule
    Given the user is on the rule editing page for "DecisionTable" and "RuleToCancel"
    And there is an existing condition named "ConditionToCancel"
    And "DecisionTable" has an existing rule "RuleToCancel"
    When the user enters specific condition values for "RuleToCancel"
    And the user cancels the entry
    Then the system should not update "RuleToCancel" with the entered values
    And the user should see a cancellation message
