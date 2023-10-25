import copy
import functools
from pywebio.input import input, select, input_group
from pywebio.output import clear, put_button, put_text, put_table

conditions = ["Condition 1"]
actions = ["Action 1"]

# Python object used for storing all the data about the current table
table_data = {
    "table_name": "My Decision Table",
    "num_conditions": 1,
    "num_actions": 1,
    "headers": ["Options", "Condition 1", "Action 1"],
    "data": [[1, True, True],
             [2, False, False]]
}

# Code to execute at launch
def main():
    # Display a 'Create table' button to the user
    put_button('Create Table', onclick=create_table)


# Creates and display the initial decision table
def create_table():
    # Prompt user to enter a table name
    table_data["table_name"] = input("How should we name this decision table?")
    
    # Updates the table visual on display
    display_table()


# Adds a new condition variable to the table
def add_condition():
    global table_data   # Uses the global value of the table data
    global conditions   # Uses the global value of the conditions list

    # Prompt user to enter a condition name
    condition_name = input("Enter a name for the condition:")

    # Update values in the table data object and conditions list
    table_data["num_conditions"] += 1
    conditions.append(condition_name)
    table_data["headers"].insert(table_data["num_conditions"], condition_name)

    # Generate all possible combinations of all conditions
    conditions_combinations = generate_combinations(table_data["num_conditions"])
    new_table_data = copy.deepcopy(conditions_combinations)

    # Go through the data array to add the remaining data (row indices and actions initial values) 
    for index in range(len(conditions_combinations)):
        new_table_data[index].insert(0, index+1)    # Insert row indices at the beginning
        for _ in range(table_data["num_actions"]):
            new_table_data[index].append(False)     # Insert the initial value for the actions

    # Update the table data object with the new values
    table_data["data"] = copy.deepcopy(new_table_data)
    
    # Updates the table visual on display
    display_table()


# Adds a new action column to the table
def add_action():
    global table_data   # Uses the global value of the table data
    global actions      # Uses the global value of the list of actions

    # Prompt user to enter an action name
    action_name = input("Enter a name for the action:")

    # Update values in the table data object and conditions list
    table_data["headers"].append(action_name)
    actions.append(action_name)
    table_data["num_actions"] += 1
    
    # Insert the initial value for the actions
    for row in table_data["data"]:
        row.append(False)
    
    # Updates the table visual on display
    display_table()

# Adds a new rule to the table
def add_rule():

    # Creates an input group pop up to input rule parameters
    inputs = input_group("Add Rule", [

        select("If [condition]", options=conditions, name="rule_condition"),    # select a conditions
        select("is [boolean]", options=[True, False], name="rule_boolean"),     # select a boolean value
        select("Then [action]", options=actions, name="rule_action"),           # select an action
        select("is [decision]", options=[True, False], name="rule_decision")    # select a boolean value

    ])

    i_c = 0     # index of where the condition is in the header of the table
    # Search through the headers of the table for a matching condition
    for header in table_data["headers"]:
        if header == inputs['rule_condition']:
            break
        else:
            i_c+=1

    i_a = 0     # index of where the action is in the header of the table
    # Search through the headers of the table for a matching action
    for header in table_data["headers"]:
        if header == inputs['rule_action']:
            break
        else: 
            i_a+=1

    i_r = 0     # index for each row in the table
    # for each row where the condition equals the input condition, update the action
    for row in table_data["data"]:
        if row[i_c] == inputs["rule_boolean"]:
            if row[i_a] != inputs["rule_decision"]:
                toggle_action(i_r, i_a)     # updates the button
        i_r+=1
    
    # Print the rule to the main page
    put_text("Rule: if {} = {}, then {} = {}".format(
        inputs['rule_condition'], inputs['rule_boolean'], inputs['rule_action'], inputs['rule_decision']))

# Gathers the information from the table_data object to properly display it 
def display_table():
    global table_data   # Uses the global value of the table data

    # table_array is used to pass to the frontend library put_table function
    table_array = copy.deepcopy(table_data["data"])

    # Go through the table data, and adjust the values as needed to display the right UI elements
    for i in range(len(table_data["data"])):
        for j in range(len(table_data["data"][i])):
            if (j > table_data["num_conditions"]):
                table_array[i][j] = put_button(table_array[i][j], onclick= functools.partial(toggle_action, i, j), color = get_color(table_array[i][j]))
    
    # Update the UI
    clear()
    put_text(table_data["table_name"])
    put_table(table_array, header=table_data["headers"])
    put_button('Add condition', onclick=add_condition)
    put_button('Add action', onclick=add_action)
    put_button('Add rule', onclick=add_rule)
    

# Toggles the value in an action column, at the specific row&column from where the user interaction came from
def toggle_action(row, column):
    if (table_data["data"][row][column]):
        table_data["data"][row][column] = False
    else : table_data["data"][row][column] = True
    display_table()


# Returns the appropriate color value based on whether a value is true or false
def get_color(value):
    if (value): return 'success'
    else: return 'danger'


# Generates all 2^n possible combinations of n boolean variables
def generate_combinations(n):
    if n == 0:
        return [[]]
    smaller_combinations = generate_combinations(n - 1)
    combinations = []
    for combination in smaller_combinations:
        combinations.append(combination + [True])
        combinations.append(combination + [False])
    return combinations
    

if __name__ == '__main__':
    main()
            