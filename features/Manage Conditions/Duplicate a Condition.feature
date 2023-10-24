Feature: Duplicate a Condition

  Scenario: User successfully duplicates an existing condition
    Given the user is on the conditions management page
    And there is an existing condition named "OriginalCondition"
    When the user selects to duplicate the condition named "OriginalCondition"
    Then the system should create a duplicate of "OriginalCondition"
    And the user should see a success message

  Scenario: User tries to duplicate a non-existent condition
    Given the user is on the conditions management page
    And there is no condition named "NonExistentCondition"
    When the user selects to duplicate the condition named "NonExistentCondition"
    Then the system should display an error message

  Scenario: User tries to duplicate a condition with an invalid name
    Given the user is on the conditions management page
    And there is an existing condition named "ExistingCondition"
    When the user selects to duplicate the condition named "ExistingCondition"
    And the user enters an invalid name for the duplicate (e.g., empty or containing special characters)
    Then the system should not create the duplicate condition
    And the user should see an error message about the invalid name

  Scenario: User cancels duplicating a condition
    Given the user is on the conditions management page
    And there is an existing condition named "ConditionToCancel"
    When the user selects to duplicate the condition named "ConditionToCancel"
    And the user cancels the duplication
    Then the system should not create the duplicate condition
    And the user should see a cancellation message
