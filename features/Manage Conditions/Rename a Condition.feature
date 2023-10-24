Feature: Rename a Condition

  Scenario: User successfully renames an existing condition
    Given the user is on the conditions management page
    And there is an existing condition named "OldConditionName"
    When the user selects to rename the condition named "OldConditionName"
    And the user enters the new name "NewConditionName"
    And the user confirms the renaming
    Then the system should rename "OldConditionName" to "NewConditionName"
    And the user should see a success message

  Scenario: User tries to rename a non-existent condition
    Given the user is on the conditions management page
    And there is no condition named "NonExistentCondition"
    When the user selects to rename the condition named "NonExistentCondition"
    And the user enters the new name "NewConditionName"
    And the user confirms the renaming
    Then the system should display an error message

  Scenario: User tries to rename a condition with an invalid name
    Given the user is on the conditions management page
    And there is an existing condition named "ExistingCondition"
    When the user selects to rename the condition named "ExistingCondition"
    And the user enters an invalid new name (e.g., empty or containing special characters)
    And the user confirms the renaming
    Then the system should not rename the condition
    And the user should see an error message about the invalid name

  Scenario: User cancels renaming a condition
    Given the user is on the conditions management page
    And there is an existing condition named "ConditionToCancel"
    When the user selects to rename the condition named "ConditionToCancel"
    And the user enters the new name "NewConditionName"
    And the user cancels the renaming
    Then the system should not rename the condition
    And the user should see a cancellation message
