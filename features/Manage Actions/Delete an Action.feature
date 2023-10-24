Feature: Delete an Action

  Scenario: User successfully deletes an existing action
    Given the user is on the actions management page
    And there is an existing action named "ActionToDelete"
    When the user selects to delete the action named "ActionToDelete"
    Then the system should confirm the deletion
    When the user confirms the deletion
    Then the system should delete the action named "ActionToDelete"
    And the user should see a success message

  Scenario: User tries to delete a non-existent action
    Given the user is on the actions management page
    And there is no action named "NonExistentAction"
    When the user selects to delete the action named "NonExistentAction"
    Then the system should display an error message

  Scenario: User cancels action deletion
    Given the user is on the actions management page
    And there is an existing action named "ActionToCancel"
    When the user selects to delete the action named "ActionToCancel"
    Then the system should confirm the deletion
    When the user cancels the deletion
    Then the system should not delete the action
    And the user should see a cancellation message

  Scenario: User tries to delete an action associated with rules
    Given the user is on the actions management page
    And there is an existing action named "ActionWithRules"
    And "ActionWithRules" is associated with rules
    When the user selects to delete the action named "ActionWithRules"
    Then the system should confirm the deletion
    When the user confirms the deletion
    Then the system should not delete the action
    And the user should see an error message about associated rules
