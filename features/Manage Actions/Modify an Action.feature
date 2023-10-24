Feature: Modify an Action

  Scenario: User successfully modifies an existing action
    Given the user is on the actions management page
    And there is an existing action named "ExistingAction"
    When the user selects to modify the action named "ExistingAction"
    And the user makes changes to the action definition
    And the user saves the modifications
    Then the system should update the action "ExistingAction" with the new definition
    And the user should see a success message

  Scenario: User tries to modify a non-existent action
    Given the user is on the actions management page
    And there is no action named "NonExistentAction"
    When the user selects to modify the action named "NonExistentAction"
    Then the system should display an error message

  Scenario: User tries to modify an action with an invalid definition
    Given the user is on the actions management page
    And there is an existing action named "ActionWithInvalidDefinition"
    When the user selects to modify the action named "ActionWithInvalidDefinition"
    And the user enters an invalid new definition
    And the user saves the modifications
    Then the system should not update the action
    And the user should see an error message about the invalid definition

  Scenario: User cancels modifying an action
    Given the user is on the actions management page
    And there is an existing action named "ActionToCancel"
    When the user selects to modify the action named "ActionToCancel"
    And the user makes changes to the action definition
    And the user cancels the modification
    Then the system should not update the action
    And the user should see a cancellation message
