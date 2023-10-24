Feature: Rename an Action

  Scenario: User successfully renames an existing action
    Given the user is on the actions management page
    And there is an existing action named "OldActionName"
    When the user selects to rename the action named "OldActionName"
    And the user enters the new name "NewActionName"
    And the user confirms the renaming
    Then the system should rename "OldActionName" to "NewActionName"
    And the user should see a success message

  Scenario: User tries to rename a non-existent action
    Given the user is on the actions management page
    And there is no action named "NonExistentAction"
    When the user selects to rename the action named "NonExistentAction"
    And the user enters the new name "NewActionName"
    And the user confirms the renaming
    Then the system should display an error message

  Scenario: User tries to rename an action with an invalid name
    Given the user is on the actions management page
    And there is an existing action named "ExistingAction"
    When the user selects to rename the action named "ExistingAction"
    And the user enters an invalid new name (e.g., empty or containing special characters)
    And the user confirms the renaming
    Then the system should not rename the action
    And the user should see an error message about the invalid name

  Scenario: User cancels renaming an action
    Given the user is on the actions management page
    And there is an existing action named "ActionToCancel"
    When the user selects to rename the action named "ActionToCancel"
    And the user enters the new name "NewActionName"
    And the user cancels the renaming
    Then the system should not rename the action
    And the user should see a cancellation message
