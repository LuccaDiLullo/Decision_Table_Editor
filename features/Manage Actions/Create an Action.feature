Feature: Create an Action

  Scenario: User successfully creates a new action
    Given the user is on the actions management page
    When the user selects to create a new action
    And the user enters the name "NewActionName" for the action
    And the user provides a description for the action
    And the user saves the new action
    Then the system should create a new action named "NewActionName"
    And the user should see a success message

  Scenario: User tries to create an action with a duplicate name
    Given the user is on the actions management page
    And there is an existing action named "ExistingAction"
    When the user selects to create a new action
    And the user enters the name "ExistingAction" for the new action
    And the user provides a description for the action
    And the user saves the new action
    Then the system should not create the new action
    And the user should see an error message about the duplicate name

  Scenario: User tries to create an action without providing a name
    Given the user is on the actions management page
    When the user selects to create a new action
    And the user does not provide a name for the action
    And the user saves the new action
    Then the system should not create the new action
    And the user should see an error message about the missing name

  Scenario: User cancels creating a new action
    Given the user is on the actions management page
    When the user selects to create a new action
    And the user cancels the creation
    Then the system should not create the new action
    And the user should see a cancellation message
