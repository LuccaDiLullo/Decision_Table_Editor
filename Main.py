import copy
import functools
from pywebio.input import input, select, input_group
from pywebio.output import clear, put_button, put_text, put_table

conditions = ["Condition1"]
actions = ["Action1"]

table_data = {
    "table_name": "My Decision Table",
    "num_conditions": 1,
    "num_actions": 1,
    "headers": ["Options", "Condition1", "Action1"],
    "data": [[1, True, True],
             [2, False, False]]
}

def main():
    put_button('Create Table', onclick=create_table)

def create_table():
    table_data["table_name"] = input("How should we name this decision table?")
    display_table()

def add_condition():
    print("condition")

def add_action():
    global table_data
    global actions
    action_name = input("Enter an action name:")
    table_data["headers"].append(action_name)
    actions.append(action_name)
    table_data["num_actions"] += 1
    
    for row in table_data["data"]:
        row.append(False)
    
    display_table()

def add_rule():
    
    inputs = input_group("Add Rule", [

        select("If [condition]", options=conditions, name="rule_condition"),
        select("is [boolean]", options=[True, False], name="rule_boolean"),
        select("Then [action]", options=actions, name="rule_action"),
        select("is [decision]", options=[True, False], name="rule_decision")

    ])

    put_text("Rule: if {} = {}, then {} = {}".format(
        inputs['rule_condition'], inputs['rule_boolean'], inputs['rule_action'], inputs['rule_decision']))
    
    i_c = 0
    for header in table_data["headers"]:
        if header == inputs['rule_condition']:
            break
        else:
            i_c+=1

    i_a = 0
    for header in table_data["headers"]:
        if header == inputs['rule_action']:
            break
        i_a+=1

    i_r = 0
    for row in table_data["data"]:
        if row[i_c] == inputs["rule_boolean"]:
            if row[i_a] != inputs["rule_decision"]:
                toggle_action(i_r, i_a)
                break
        i_r+=1
        

def display_table():
    global table_data
    table_array = copy.deepcopy(table_data["data"])
    for i in range(len(table_data["data"])):
        for j in range(len(table_data["data"][i])):
            if (j > table_data["num_conditions"]):
                table_array[i][j] = put_button(table_array[i][j], onclick= functools.partial(toggle_action, i, j), color = get_color(table_array[i][j]))
    
    clear()
    put_text(table_data["table_name"])
    put_table(table_array, header=table_data["headers"])
    put_button('Add condition', onclick=add_condition)
    put_button('Add action', onclick=add_action)
    put_button('Add Rule', onclick=add_rule)
    

def toggle_action(row, column):
    if (table_data["data"][row][column]):
        table_data["data"][row][column] = False
    else : table_data["data"][row][column] = True
    display_table()

def get_color(value):
    if (value): return 'success'
    else: return 'danger'
    
if __name__ == '__main__':
    main()