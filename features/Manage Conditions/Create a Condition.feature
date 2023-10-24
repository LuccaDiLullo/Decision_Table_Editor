Feature: Create a Condition

  Scenario: User successfully creates a new condition
    Given the user is on the conditions management page
    When the user selects to create a new condition
    And the user enters the name "NewConditionName" for the condition
    And the user provides a description for the condition
    And the user saves the new condition
    Then the system should create a new condition named "NewConditionName"
    And the user should see a success message

  Scenario: User tries to create a condition with a duplicate name
    Given the user is on the conditions management page
    And there is an existing condition named "ExistingCondition"
    When the user selects to create a new condition
    And the user enters the name "ExistingCondition" for the new condition
    And the user provides a description for the condition
    And the user saves the new condition
    Then the system should not create the new condition
    And the user should see an error message about the duplicate name

  Scenario: User tries to create a condition without providing a name
    Given the user is on the conditions management page
    When the user selects to create a new condition
    And the user does not provide a name for the condition
    And the user saves the new condition
    Then the system should not create the new condition
    And the user should see an error message about the missing name

  Scenario: User cancels creating a new condition
    Given the user is on the conditions management page
    When the user selects to create a new condition
    And the user cancels the creation
    Then the system should not create the new condition
    And the user should see a cancellation message
