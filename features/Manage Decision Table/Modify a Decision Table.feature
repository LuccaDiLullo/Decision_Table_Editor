Feature: Modify a Decision Table

  Scenario: User successfully modifies an existing decision table
    Given the user is on the decision tables management page
    And there is an existing decision table named "ExistingDecisionTable"
    When the user selects to modify the decision table named "ExistingDecisionTable"
    And the user makes changes to the decision logic
    And the user saves the modifications
    Then the system should update the decision table with the new logic
    And the user should see a success message

  Scenario: User cancels modification of a decision table
    Given the user is on the decision tables management page
    And there is an existing decision table named "DecisionTableToCancel"
    When the user selects to modify the decision table named "DecisionTableToCancel"
    And the user makes changes to the decision logic
    And the user cancels the modification
    Then the system should not update the decision table
    And the user should see a cancellation message

  Scenario: User tries to modify a non-existent decision table
    Given the user is on the decision tables management page
    And there is no decision table named "NonExistentDecisionTable"
    When the user selects to modify the decision table named "NonExistentDecisionTable"
    Then the system should display an error message

  Scenario: User modifies a decision table with associated rules
    Given the user is on the decision tables management page
    And there is an existing decision table named "TableWithAssociatedRules"
    And "TableWithAssociatedRules" has associated rules
    When the user selects to modify the decision table named "TableWithAssociatedRules"
    And the user makes changes to the decision logic
    And the user saves the modifications
    Then the system should update the decision table and its associated rules
    And the user should see a success message
