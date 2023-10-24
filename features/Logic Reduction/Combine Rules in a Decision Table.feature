Feature: Combine Rules in a Decision Table

  Scenario: User successfully combines two existing rules in a decision table
    Given the user is on the decision table editing page for "DecisionTable"
    And "DecisionTable" has existing rules "Rule1" and "Rule2"
    When the user selects to combine "Rule1" and "Rule2" into a single rule
    And the user specifies the conditions and actions for the combined rule
    And the user saves the combined rule
    Then the system should create a new combined rule in "DecisionTable"
    And the user should see a success message
    And "Rule1" and "Rule2" should be removed from "DecisionTable"

  Scenario: User tries to combine non-existent rules in a decision table
    Given the user is on the decision table editing page for "DecisionTable"
    And there is no rule named "NonExistentRule" in "DecisionTable"
    When the user tries to combine "NonExistentRule" with another rule
    Then the system should display an error message

  Scenario: User cancels combining rules in a decision table
    Given the user is on the decision table editing page for "DecisionTable"
    And "DecisionTable" has existing rules "RuleToCancel1" and "RuleToCancel2"
    When the user selects to combine "RuleToCancel1" and "RuleToCancel2" into a single rule
    And the user cancels the combining process
    Then the system should not create a new combined rule
    And the user should see a cancellation message
    And "RuleToCancel1" and "RuleToCancel2" should remain in "DecisionTable"
