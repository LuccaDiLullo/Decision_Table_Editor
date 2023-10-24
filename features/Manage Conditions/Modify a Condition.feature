Feature: Modify a Condition

  Scenario: User successfully modifies an existing condition
    Given the user is on the conditions management page
    And there is an existing condition named "ExistingCondition"
    When the user selects to modify the condition named "ExistingCondition"
    And the user makes changes to the condition definition
    And the user saves the modifications
    Then the system should update the condition "ExistingCondition" with the new definition
    And the user should see a success message

  Scenario: User tries to modify a non-existent condition
    Given the user is on the conditions management page
    And there is no condition named "NonExistentCondition"
    When the user selects to modify the condition named "NonExistentCondition"
    Then the system should display an error message

  Scenario: User tries to modify a condition with an invalid definition
    Given the user is on the conditions management page
    And there is an existing condition named "ConditionWithInvalidDefinition"
    When the user selects to modify the condition named "ConditionWithInvalidDefinition"
    And the user enters an invalid new definition
    And the user saves the modifications
    Then the system should not update the condition
    And the user should see an error message about the invalid definition

  Scenario: User cancels modifying a condition
    Given the user is on the conditions management page
    And there is an existing condition named "ConditionToCancel"
    When the user selects to modify the condition named "ConditionToCancel"
    And the user makes changes to the condition definition
    And the user cancels the modification
    Then the system should not update the condition
    And the user should see a cancellation message
