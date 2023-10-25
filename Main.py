import copy
import functools
from pywebio.input import input, select, input_group
from pywebio.output import clear, put_button, put_text, put_table

# Initialize default conditions and actions for the table
conditions = ["Condition 1"]
actions = ["Action 1"]

# Initialize default table structure
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
    """Capture table name and display it."""
    table_name = "How should we name this decision table?"
    table_data["table_name"] = input(table_name)
    display_table()


def add_condition():
    """Add new condition to table."""
    global table_data, conditions
    condition_name = input("Enter a name for the condition:")
    table_data["num_conditions"] += 1
    conditions.append(condition_name)
    position = table_data["num_conditions"]
    table_data["headers"].insert(position, condition_name)

    # Generate new table combinations
    conditions_combinations=generate_combinations(table_data["num_conditions"])
    new_table_data = copy.deepcopy(conditions_combinations)
    for idx, combo in enumerate(conditions_combinations):
        new_table_data[idx].insert(0, idx + 1)
        new_table_data[idx].extend([False] * table_data["num_actions"])

    table_data["data"] = copy.deepcopy(new_table_data)
    display_table()


def add_action():
    """Add new action to table."""
    global table_data, actions
    action_name = input("Enter a name for the action:")
    table_data["headers"].append(action_name)
    actions.append(action_name)
    table_data["num_actions"] += 1

    # Add False for new action in each row
    for row in table_data["data"]:
        row.append(False)

    display_table()


def add_rule():
    """Capture rule from user and update table."""
    inputs = input_group("Add Rule", [
        select("If [condition]", options=conditions, name="rule_condition"),
        select("is [boolean]", options=[True, False], name="rule_boolean"),
        select("Then [action]", options=actions, name="rule_action"),
        select("is [decision]", options=[True, False], name="rule_decision")
    ])

    condition_index = table_data["headers"].index(inputs['rule_condition'])
    action_index = table_data["headers"].index(inputs['rule_action'])

    for row_index, row in enumerate(table_data["data"]):
        if row[condition_index] == inputs["rule_boolean"]:
            if row[action_index] != inputs["rule_decision"]:
                toggle_action(row_index, action_index)

    rule_display = (f"Rule: if {inputs['rule_condition']} = "
                    f"{inputs['rule_boolean']}, then {inputs['rule_action']}="
                    f"{inputs['rule_decision']}")
    put_text(rule_display)


def display_table():
    """Display the current decision table."""
    table_array = copy.deepcopy(table_data["data"])

    # Convert boolean values to buttons
    for i in range(len(table_data["data"])):
        for j in range(len(table_data["data"][i])):
            if j > table_data["num_conditions"]:
                btn = put_button(
                    table_array[i][j],
                    onclick=functools.partial(toggle_action, i, j),
                    color=get_color(table_array[i][j])
                )
                table_array[i][j] = btn

    clear()
    put_text(table_data["table_name"])
    put_table(table_array, header=table_data["headers"])
    put_button('Add condition', onclick=add_condition)
    put_button('Add action', onclick=add_action)
    put_button('Add rule', onclick=add_rule)


def toggle_action(row, column):
    """Change action's boolean value in the table."""
    table_data["data"][row][column] = not table_data["data"][row][column]
    display_table()


def get_color(value):
    """Get button color based on its value."""
    return 'success' if value else 'danger'


def generate_combinations(n):
    """Generate 2^n boolean combinations."""
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
