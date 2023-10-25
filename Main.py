import copy
import functools
from pywebio.input import input, select, input_group
from pywebio.output import clear, put_button, put_text, put_table

# Initialize conditions and actions for the table
conditions = ["Condition 1"]
actions = ["Action 1"]

# Initial table data structure
table_data = {
    "table_name": "My Decision Table",
    "num_conditions": 1,
    "num_actions": 1,
    "headers": ["Options", "Condition 1", "Action 1"],
    "data": [[1, True, True], [2, False, False]]
}


def main():
    """Display the initial 'Create table' button."""
    put_button('Create Table', onclick=create_table)


def create_table():
    """Prompt user for table name and display the table."""
    table_data["table_name"] = input("How should we name this decision table?")
    display_table()


def add_condition():
    """Add a new condition variable to the table."""
    global table_data, conditions

    condition_name = input("Enter a name for the condition:")
    table_data["num_conditions"] += 1
    conditions.append(condition_name)
    table_data["headers"].insert(table_data["num_conditions"], condition_name)

    conditions_combinations = generate_combinations(table_data["num_conditions"])
    new_table_data = copy.deepcopy(conditions_combinations)
    for index in range(len(conditions_combinations)):
        new_table_data[index].insert(0, index + 1)
        for _ in range(table_data["num_actions"]):
            new_table_data[index].append(False)

    table_data["data"] = copy.deepcopy(new_table_data)
    display_table()


def add_action():
    """Add a new action column to the table."""
    global table_data, actions

    action_name = input("Enter a name for the action:")
    table_data["headers"].append(action_name)
    actions.append(action_name)
    table_data["num_actions"] += 1

    for row in table_data["data"]:
        row.append(False)

    display_table()


def add_rule():
    """Add a new rule to the table based on user inputs."""
    inputs = input_group("Add Rule", [
        select("If [condition]", options=conditions, name="rule_condition"),
        select("is [boolean]", options=[True, False], name="rule_boolean"),
        select("Then [action]", options=actions, name="rule_action"),
        select("is [decision]", options=[True, False], name="rule_decision")
    ])

    i_c = next((i for i, header in enumerate(table_data["headers"]) if header == inputs['rule_condition']), None)
    i_a = next((i for i, header in enumerate(table_data["headers"]) if header == inputs['rule_action']), None)

    for i_r, row in enumerate(table_data["data"]):
        if row[i_c] == inputs["rule_boolean"]:
            if row[i_a] != inputs["rule_decision"]:
                toggle_action(i_r, i_a)

    put_text(f"Rule: if {inputs['rule_condition']} = {inputs['rule_boolean']}, "
             f"then {inputs['rule_action']} = {inputs['rule_decision']}")


def display_table():
    """Display the decision table with its current data."""
    table_array = copy.deepcopy(table_data["data"])

    for i in range(len(table_data["data"])):
        for j in range(len(table_data["data"][i])):
            if j > table_data["num_conditions"]:
                table_array[i][j] = put_button(
                    table_array[i][j],
                    onclick=functools.partial(toggle_action, i, j),
                    color=get_color(table_array[i][j])
                )

    clear()
    put_text(table_data["table_name"])
    put_table(table_array, header=table_data["headers"])
    put_button('Add condition', onclick=add_condition)
    put_button('Add action', onclick=add_action)
    put_button('Add rule', onclick=add_rule)


def toggle_action(row, column):
    """Toggle the value in an action column."""
    table_data["data"][row][column] = not table_data["data"][row][column]
    display_table()


def get_color(value):
    """Return color based on boolean value."""
    return 'success' if value else 'danger'


def generate_combinations(n):
    """Generate all 2^n possible combinations of n boolean variables."""
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
