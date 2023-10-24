Feature: Duplicate an Action

  Scenario: User successfully duplicates an existing action
    Given the user is on the actions management page
    And there is an existing action named "OriginalAction"
    When the user selects to duplicate the action named "OriginalAction"
    Then the system should create a duplicate of "OriginalAction"
    And the user should see a success message

  Scenario: User tries to duplicate a non-existent action
    Given the user is on the actions management page
    And there is no action named "NonExistentAction"
    When the user selects to duplicate the action named "NonExistentAction"
    Then the system should display an error message

  Scenario: User tries to duplicate an action with an invalid name
    Given the user is on the actions management page
    And there is an existing action named "ExistingAction"
    When the user selects to duplicate the action named "ExistingAction"
    And the user enters an invalid name for the duplicate (e.g., empty or containing special characters)
    Then the system should not create the duplicate action
    And the user should see an error message about the invalid name

  Scenario: User cancels duplicating an action
    Given the user is on the actions management page
    And there is an existing action named "ActionToCancel"
    When the user selects to duplicate the action named "ActionToCancel"
    And the user cancels the duplication
    Then the system should not create the duplicate action
    And the user should see a cancellation message
