Feature: Rename a Decision Table

  Scenario: User successfully renames a decision table
    Given the user is on the decision tables management page
    And there is an existing decision table named "OldDecisionTableName"
    When the user selects to rename the decision table named "OldDecisionTableName"
    And the user enters the new name "NewDecisionTableName"
    And the user confirms the renaming
    Then the system should rename "OldDecisionTableName" to "NewDecisionTableName"
    And the user should see a success message

  Scenario: User tries to rename a non-existent decision table
    Given the user is on the decision tables management page
    And there is no decision table named "NonExistentTable"
    When the user selects to rename the decision table named "NonExistentTable"
    And the user enters the new name "NewDecisionTableName"
    And the user confirms the renaming
    Then the system should display an error message

  Scenario: User tries to rename a decision table with an invalid name
    Given the user is on the decision tables management page
    And there is an existing decision table named "ExistingTable"
    When the user selects to rename the decision table named "ExistingTable"
    And the user enters an invalid new name (e.g., empty or containing special characters)
    And the user confirms the renaming
    Then the system should not rename the decision table
    And the user should see an error message about the invalid name

  Scenario: User cancels renaming a decision table
    Given the user is on the decision tables management page
    And there is an existing decision table named "DecisionTableToCancel"
    When the user selects to rename the decision table named "DecisionTableToCancel"
    And the user enters the new name "NewDecisionTableName"
    And the user cancels the renaming
    Then the system should not rename the decision table
    And the user should see a cancellation message
