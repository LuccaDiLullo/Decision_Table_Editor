Feature: Delete a Condition

  Scenario: User successfully deletes an existing condition
    Given the user is on the conditions management page
    And there is an existing condition named "ConditionToDelete"
    When the user selects to delete the condition named "ConditionToDelete"
    Then the system should confirm the deletion
    When the user confirms the deletion
    Then the system should delete the condition named "ConditionToDelete"
    And the user should see a success message

  Scenario: User tries to delete a non-existent condition
    Given the user is on the conditions management page
    And there is no condition named "NonExistentCondition"
    When the user selects to delete the condition named "NonExistentCondition"
    Then the system should display an error message

  Scenario: User cancels condition deletion
    Given the user is on the conditions management page
    And there is an existing condition named "ConditionToCancel"
    When the user selects to delete the condition named "ConditionToCancel"
    Then the system should confirm the deletion
    When the user cancels the deletion
    Then the system should not delete the condition
    And the user should see a cancellation message

  Scenario: User tries to delete a condition associated with rules
    Given the user is on the conditions management page
    And there is an existing condition named "ConditionWithRules"
    And "ConditionWithRules" is associated with rules
    When the user selects to delete the condition named "ConditionWithRules"
    Then the system should confirm the deletion
    When the user confirms the deletion
    Then the system should not delete the condition
    And the user should see an error message about associated rules
