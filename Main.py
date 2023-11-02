import copy
import functools
from pywebio.input import input, select, input_group, textarea
from pywebio.output import clear, put_button, put_text, put_table

conditions = []
actions = []

# Python object used for storing all the data about the current table
table_data = {
    "table_name": "My Decision Table",
    "num_conditions": 0,
    "num_actions": 0,
    "num_rules": 0,
    "headers": ["Rules", " "],
    "data": [["Conditions", " "], ["Actions", " "]]
}

# Code to execute at launch
def main():
    # Display a 'Create table' button to the user
    put_button('Create Table', onclick=create_table)


# Creates and display the initial decision table
def create_table():
    # Prompt user to enter a table name
    table_data["table_name"] = input("Name this decision table?", validate=naming)
    
    # Updates the table visual on display
    display_table()

def naming(name):
    if len(name) < 1 or len(name) > 32:
        return "Name must be between 1 than 32 characters"


# Adds a new condition variable to the table
def add_condition():
    global table_data   # Uses the global value of the table data
    global conditions   # Uses the global value of the conditions list

    # Prompt user to enter a condition name
    inputs = input_group("Add Condition", [

        input("Enter a name for the condition:", name="condition_name", validate=naming),
        select("Slect the type of variable", options=["True/False", "Number"], name="condition_type"),    # select a conditions

    ])

    # Update values in the table data object and conditions list
    table_data["num_conditions"] += 1
    postition = table_data["num_conditions"]
    table_data["data"].insert(postition, [" ", inputs["condition_name"]])

    # Update rules
    if table_data["num_rules"] != 0:
        for _ in range(table_data["num_rules"]):
            if inputs["condition_type"] == "True/False":
                table_data["data"][postition].append(False)
            else:
                table_data["data"][postition].append(0)
            
    # Add this condition to the global conditions list
    conditions.append([inputs["condition_name"], inputs["condition_type"]])
    
    # Updates the table visual on display
    display_table()

# Adds a new action row to the table
def add_action():
    global table_data   # Uses the global value of the table data
    global actions      # Uses the global value of the actions list

    # Prompt user to enter a condition name
    inputs = input_group("Add Action", [

        input("Enter a name for the action:", name="action_name", validate=naming),
        select("Slect the type of variable", options=["True/False", "Number"], name="action_type"),    # select a conditions

    ])

    # Update values in the table data object and conditions list
    table_data["num_actions"] += 1
    postition = table_data["num_conditions"] + table_data["num_actions"] + 1
    table_data["data"].insert(postition, [" ", inputs["action_name"]])

    # Update rules
    if table_data["num_rules"] != 0:
        for _ in range(table_data["num_rules"]):
            if inputs["action_type"] == "True/False":
                table_data["data"][postition].append(False)
            else:
                table_data["data"][postition].append(0)

    # Add this condition to the global actions list
    actions.append([inputs["action_name"], inputs["action_type"]])
    
    # Updates the table visual on display
    display_table()

# Adds a new rule column to the table
def add_rule():
    global table_data   # Uses the global value of the table data
    global conditions   # Uses the global value of the conditions list
    global actions      # Uses the global value of the actions list

    if actions == [] and conditions == []:
        put_text("Create a condition or an action first!")

    else:
        # Update values in the table data object and conditions list
        table_data["num_rules"] += 1 
        table_data["headers"].append(table_data["num_rules"])
        for row in table_data["data"]:
            if row[0] != " ":
                    row.append(" ")
            
            # check the type of condition and fill default
            for condition in conditions:
                if condition[0] == row[1] and condition[1] == "True/False":
                    row.append(False)
                elif condition[0] == row[1] and condition[1] == "Number":
                    row.append(0)
            
            # check the type of actiona and fill default
            for action in actions:
                if action[0] == row[1] and action[1] == "True/False":
                    row.append(False)
                elif action[0] == row[1] and action[1] == "Number":
                    row.append(0)
        
        # Updates the table visual on display
        display_table()

# Creates a Logical Expression
def logic_expression():

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
                toggle_boolean(i_r, i_a)     # updates the button
        i_r+=1
    
    # Print the rule to the main page
    put_text("Rule: if {} = {}, then {} = {}".format(
        inputs['rule_condition'], inputs['rule_boolean'], inputs['rule_action'], inputs['rule_decision']))

# Gathers the information from the table_data object to properly display it 
def display_table():
    global table_data   # Uses the global value of the table data

    # table_array is used to pass to the data library put_table function
    table_array = copy.deepcopy(table_data["data"])

    # Go through the table data, and adjust the values as needed to display the right UI elements
    for i in range(len(table_data["data"])):
        for j in range(len(table_data["data"][i])):
            if table_array[i][j] is True or table_array[i][j] is False:
                table_array[i][j] = put_button(table_array[i][j], onclick= functools.partial(toggle_boolean, i, j), color = get_color(table_array[i][j]))

    # Update the UI
    clear()
    put_text(table_data["table_name"])
    put_table(table_array, header=table_data["headers"])

    put_button('Add condition', onclick=add_condition)
    put_button('Add action', onclick=add_action)
    put_button('Add rule', onclick=add_rule)
    # put_button('Add Logical Expression', onclick=logic_expression)
    

# Toggles the value in an action column, at the specific row&column from where the user interaction came from
def toggle_boolean(row, column):
    if (table_data["data"][row][column]):
        table_data["data"][row][column] = False
    else : 
        table_data["data"][row][column] = True
    
    # Updates the table visual on display
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
            