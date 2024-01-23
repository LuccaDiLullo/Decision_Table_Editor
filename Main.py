import json
import copy
import functools
from pywebio.input import input, select, input_group, NUMBER, input_update, FLOAT, file_upload
from pywebio.output import clear, put_button, put_text, put_table, style, put_row

number2attributes = {
    'Integer': ['Integer'],
    'Range': ['Inclusive', 'Exclusive'],
    'Decimal': ["1", "2", "3"]
}

# Initialize default table structure
table_data = {
    "table_name": "My Decision Table",
    "num_conditions": 0,
    "conditions": [],
    "num_actions": 0,
    "actions": [],
    "custom": {},
    "num_rules": 0,
    "headers": ["Rules", " "],
    "data": [["Conditions", " "], ["Actions", " "]]
}

opened_file = None

def main():
    #Display the initial 'Create table' button.
    clear()
    put_button('Create Table', onclick=create_table)
    put_button('Open Table', onclick=open_table)


def create_table():
    # Prompt user to enter a table name
    table_data["table_name"] = input("Name this decision table", validate=naming)

    # Updates the table visual on display
    save(table_data)
    display_table()

def open_table():
    global table_data, opened_file
    # Prompt user to enter a table name
    opened_file = file_upload("Select .json file to open", accept=".json")
    table_data = json.loads(opened_file['content'])
    
    print(table_data)
    # Updates the table visual on display
    display_table()

def naming(name):
    if len(name) < 1 or len(name) > 32:
        return "Name must be between 1 than 32 characters"

def add_condition():
    global table_data   # Uses the global value of the table data
    global number2attributes # Uses the global value for number types

    # Prompt user to enter a condition name
    inputs = input_group("Add Condition", [
        input("Enter a name for the condition:", name="condition_name", validate=naming),
        select("Select the type of variable", options=["True/False", "Number", "Custom"], name="condition_type"),    # select a conditions
    ])

    if inputs["condition_type"] == "Number":
        number_types = list(number2attributes.keys())
        num_inputs_types = input_group('Select a type:', [
            select('Number type', options=number_types, name='type', onchange=lambda c: input_update('attributes', options=number2attributes[c])),
            select('Attributes', options=number2attributes[number_types[0]], name='attributes'),
        ])

    if inputs["condition_type"] == "Custom":
        if table_data['custom'] == {}:
            put_text("Create a custom type first")
        else:
            custom_types = list(table_data['custom'].keys())
            cus_inputs_types = input_group('Select a type:', [
                select('Custom type', options=custom_types, name='type'),
            ])

    # Update values in the table data object and conditions list
    table_data["num_conditions"] += 1
    position = table_data["num_conditions"]
    table_data["data"].insert(position, [" ", inputs["condition_name"]])

    # Update rules
    if table_data["num_rules"] != 0:
        for _ in range(table_data["num_rules"]):
            if inputs["condition_type"] == "True/False":
                table_data["data"][position].append("False")
            elif inputs["condition_type"] == "Number":
                match num_inputs_types["type"]:
                    case "Integer": table_data["data"][position].append(0)
                    case "Range": 
                        if num_inputs_types['attributes'] == "Inclusive":
                            table_data["data"][position].append('[0,0]')
                        else: table_data["data"][position].append(']0,0[')
                    case "Decimal": 
                        match num_inputs_types['attributes']:
                            case "1": table_data["data"][position].append('0.0')
                            case "2": table_data["data"][position].append('0.00')
                            case "3": table_data["data"][position].append('0.000')
            elif inputs["condition_type"] == "Custom":
                table_data["data"][position].append(table_data['custom'][cus_inputs_types["type"]][0])
            
    # Add this condition to the global conditions list
    if inputs["condition_type"] == "True/False":
        table_data['conditions'].append([inputs["condition_name"], inputs["condition_type"]])
    elif inputs["condition_type"] == "Number": 
        table_data['conditions'].append([inputs["condition_name"], num_inputs_types["attributes"]])
    elif inputs["condition_type"] == "Custom":
        table_data['conditions'].append([inputs["condition_name"], cus_inputs_types["type"]])
    
    # Updates the table visual on display
    save(table_data)
    display_table()

def modify_condition(row, column):
    global table_data
    
    cur_name = table_data["data"][row][column]
    index = 0

    for condition in table_data['conditions']:
        if condition[0] == cur_name: 
            index = table_data['conditions'].index(condition)
            break
    
    inputs = input_group("Modify Condition", [
        select("Would you like to edit the name?", options=["Yes", "No"], name="name", validate=naming),
        select("Would you like to edit the type?", options=["Yes", "No"], name="type", validate=naming)
    ])

    # EDIT BOTH
    if inputs["name"] == "Yes" and inputs["type"] == "Yes": 
        new_vars = input_group("Add Condition", [
            input("Enter a new name for the condition", name="condition_name", validate=naming),
            select("Select a new type", options=["True/False", "Number", "Custom"], name="condition_type"),    # select a conditions
        ])

        if new_vars["condition_type"] == "Number":
            number_types = list(number2attributes.keys())
            num_inputs_types = input_group('Select a type:', [
                select('Number type', options=number_types, name='type', onchange=lambda c: input_update('attributes', options=number2attributes[c])),
                select('Attributes', options=number2attributes[number_types[0]], name='attributes'),
            ])

        if new_vars["condition_type"] == "Custom":
            if table_data['custom'] == {}:
                put_text("Create a custom type first")
            else:
                custom_types = list(table_data['custom'].keys())
                cus_inputs_types = input_group('Select a type:', [
                    select('Custom type', options=custom_types, name='type'),
                ])

        table_data["data"][row][column] = new_vars["condition_name"]
        table_data["conditions"][index][0] = new_vars["condition_name"]
        
        # Update rules
        if table_data["num_rules"] != 0:
            for i in range(2, table_data["num_rules"]+2):
                if new_vars["condition_type"] == "True/False":
                    table_data["conditions"][index][1] = new_vars["condition_type"]
                    table_data["data"][row][i] = "False"
                elif new_vars["condition_type"] == "Number":
                    match num_inputs_types["type"]:
                        case "Integer": 
                            table_data["conditions"][index][1] = num_inputs_types["attributes"]
                            table_data["data"][row][i] = 0
                        case "Range": 
                            if num_inputs_types['attributes'] == "Inclusive":
                                table_data["conditions"][index][1] = num_inputs_types["attributes"]
                                table_data["data"][row][i] = "[0,0]"
                            else: 
                                table_data["conditions"][index][1] = num_inputs_types["attributes"]
                                table_data["data"][row][i] = "]0,0["
                        case "Decimal": 
                            match num_inputs_types['attributes']:
                                case "1": 
                                    table_data["conditions"][index][1] = num_inputs_types["attributes"]
                                    table_data["data"][row][i] = "0.0"
                                case "2": 
                                    table_data["conditions"][index][1] = num_inputs_types["attributes"]
                                    table_data["data"][row][i] = "0.00"
                                case "3": 
                                    table_data["conditions"][index][1] = num_inputs_types["attributes"]
                                    table_data["data"][row][i] = "0.000"
                elif new_vars["condition_type"] == "Custom":
                    table_data["conditions"][index][1] = cus_inputs_types["type"]
                    table_data["data"][row][i] = table_data['custom'][cus_inputs_types["type"]][0]
        
    # EDIT NAME ONLY
    elif inputs["name"] == "Yes" and inputs["type"] == "No":
        new_name = input_group("Modify this condition", [
            input("Enter a new name for the condition", name="condition_name", validate=naming),
        ])
        table_data["conditions"][index][0] = new_name["condition_name"]
        table_data["data"][row][column] = new_name["condition_name"]
    
    # EDIT TYPE ONLY
    elif inputs["type"] == "Yes" and inputs["name"] == "No":
        new_type = input_group("Modify this confition", [
            select("Select a new type", options=["True/False", "Number", "Custom"], name="condition_type"),    # select a conditions
        ])

        if new_type["condition_type"] == "Number":
            number_types = list(number2attributes.keys())
            num_inputs_types = input_group('Select a type:', [
                select('Number type', options=number_types, name='type', onchange=lambda c: input_update('attributes', options=number2attributes[c])),
                select('Attributes', options=number2attributes[number_types[0]], name='attributes'),
            ])

        if new_type["condition_type"] == "Custom":
            if table_data['custom'] == {}:
                put_text("Create a custom type first")
            else:
                custom_types = list(table_data['custom'].keys())
                cus_inputs_types = input_group('Select a type:', [
                    select('Custom type', options=custom_types, name='type'),
                ])

        # Update rules
        if table_data["num_rules"] != 0:
            for i in range(2, table_data["num_rules"]+2):
                if new_type["condition_type"] == "True/False":
                    table_data["conditions"][index][1] = new_type["condition_type"]
                    table_data["data"][row][i] = "False"
                elif new_type["condition_type"] == "Number":
                    match num_inputs_types["type"]:
                        case "Integer": 
                            table_data["conditions"][index][1] = num_inputs_types["attributes"]
                            table_data["data"][row][i] = 0
                        case "Range": 
                            if num_inputs_types['attributes'] == "Inclusive":
                                table_data["conditions"][index][1] = num_inputs_types["attributes"]
                                table_data["data"][row][i] = "[0,0]"
                            else: 
                                table_data["conditions"][index][1] = num_inputs_types["attributes"]
                                table_data["data"][row][i] = "]0,0["
                        case "Decimal": 
                            match num_inputs_types['attributes']:
                                case "1": 
                                    table_data["conditions"][index][1] = num_inputs_types["attributes"]
                                    table_data["data"][row][i] = "0.0"
                                case "2": 
                                    table_data["conditions"][index][1] = num_inputs_types["attributes"]
                                    table_data["data"][row][i] = "0.00"
                                case "3": 
                                    table_data["conditions"][index][1] = num_inputs_types["attributes"]
                                    table_data["data"][row][i] = "0.000"
                elif new_type["condition_type"] == "Custom":
                    table_data["conditions"][index][1] = cus_inputs_types["type"]
                    table_data["data"][row][i] = table_data['custom'][cus_inputs_types["type"]][0]
    
    save(table_data)
    display_table()

def modify_action(row, column):
    global table_data

    cur_name = table_data["data"][row][column]
    index = 0

    for action in table_data['actions']:
        if action[0] == cur_name: 
            index = table_data['actions'].index(action)
            break
    
    inputs = input_group("Modify Action", [
        select("Would you like to edit the name?", options=["Yes", "No"], name="name", validate=naming),
        select("Would you like to edit the type?", options=["Yes", "No"], name="type", validate=naming)
    ])

    # EDIT BOTH
    if inputs["name"] == "Yes" and inputs["type"] == "Yes": 
        new_vars = input_group("Add Action", [
            input("Enter a new name for the action", name="action_name", validate=naming),
            select("Select a new type", options=["True/False", "Number", "Custom"], name="action_type"),    # select an action
        ])

        if new_vars["action_type"] == "Number":
            number_types = list(number2attributes.keys())
            num_inputs_types = input_group('Select a type:', [
                select('Number type', options=number_types, name='type', onchange=lambda c: input_update('attributes', options=number2attributes[c])),
                select('Attributes', options=number2attributes[number_types[0]], name='attributes'),
            ])

        if new_vars["action_type"] == "Custom":
            if table_data['custom'] == {}:
                put_text("Create a custom type first")
            else:
                custom_types = list(table_data['custom'].keys())
                cus_inputs_types = input_group('Select a type:', [
                    select('Custom type', options=custom_types, name='type'),
                ])

        table_data["data"][row][column] = new_vars["action_name"]
        table_data["actions"][index][0] = new_vars["action_name"]
        
        # Update rules
        if table_data["num_rules"] != 0:
            for i in range(table_data["num_rules"]):
                if new_vars["action_type"] == "True/False":
                    table_data["actions"][index][1] = new_vars["action_type"]
                    table_data["data"][row][i+2] = "False"
                elif new_vars["action_type"] == "Number":
                    match num_inputs_types["type"]:
                        case "Integer": 
                            table_data["actions"][index][1] = num_inputs_types["attributes"]
                            table_data["data"][row][i+2] = 0
                        case "Range": 
                            if num_inputs_types['attributes'] == "Inclusive":
                                table_data["actions"][index][1] = num_inputs_types["attributes"]
                                table_data["data"][row][i+2] = "[0,0]"
                            else: 
                                table_data["actions"][index][1] = num_inputs_types["attributes"]
                                table_data["data"][row][i+2] = "]0,0["
                        case "Decimal": 
                            match num_inputs_types['attributes']:
                                case "1": 
                                    table_data["actions"][index][1] = num_inputs_types["attributes"]
                                    table_data["data"][row][i+2] = "0.0"
                                case "2": 
                                    table_data["actions"][index][1] = num_inputs_types["attributes"]
                                    table_data["data"][row][i+2] = "0.00"
                                case "3": 
                                    table_data["actions"][index][1] = num_inputs_types["attributes"]
                                    table_data["data"][row][i+2] = "0.000"
                elif new_vars["action_type"] == "Custom":
                    table_data["actions"][index][1] = cus_inputs_types["type"]
                    table_data["data"][row][i+2] = table_data['custom'][cus_inputs_types["type"]][0]
        
    # EDIT NAME ONLY
    elif inputs["name"] == "Yes" and inputs["type"] == "No":
        new_name = input_group("Modify this action", [
            input("Enter a new name for the action", name="action_name", validate=naming),
        ])
        table_data["actions"][index][0] = new_name["action_name"]
        table_data["data"][row][column] = new_name["action_name"]
    
    # EDIT TYPE ONLY
    elif inputs["type"] == "Yes" and inputs["name"] == "No":
        new_type = input_group("Modify this action", [
            select("Select a new type", options=["True/False", "Number", "Custom"], name="action_type"),    # select an action
        ])

        if new_type["action_type"] == "Number":
            number_types = list(number2attributes.keys())
            num_inputs_types = input_group('Select a type:', [
                select('Number type', options=number_types, name='type', onchange=lambda c: input_update('attributes', options=number2attributes[c])),
                select('Attributes', options=number2attributes[number_types[0]], name='attributes'),
            ])

        if new_type["action_type"] == "Custom":
            if table_data['custom'] == {}:
                put_text("Create a custom type first")
            else:
                custom_types = list(table_data['custom'].keys())
                cus_inputs_types = input_group('Select a type:', [
                    select('Custom type', options=custom_types, name='type'),
                ])

        # Update rules
        if table_data["num_rules"] != 0:
            for i in range(table_data["num_rules"]):
                if new_type["action_type"] == "True/False":
                    table_data["actions"][index][1] = new_type["action_type"]
                    table_data["data"][row][i+2] = "False"
                elif new_type["action_type"] == "Number":
                    match num_inputs_types["type"]:
                        case "Integer": 
                            table_data["actions"][index][1] = num_inputs_types["attributes"]
                            table_data["data"][row][i+2] = 0
                        case "Range": 
                            if num_inputs_types['attributes'] == "Inclusive":
                                table_data["actions"][index][1] = num_inputs_types["attributes"]
                                table_data["data"][row][i+2] = "[0,0]"
                            else: 
                                table_data["actions"][index][1] = num_inputs_types["attributes"]
                                table_data["data"][row][i+2] = "]0,0["
                        case "Decimal": 
                            match num_inputs_types['attributes']:
                                case "1": 
                                    table_data["actions"][index][1] = num_inputs_types["attributes"]
                                    table_data["data"][row][i+2] = "0.0"
                                case "2": 
                                    table_data["actions"][index][1] = num_inputs_types["attributes"]
                                    table_data["data"][row][i+2] = "0.00"
                                case "3": 
                                    table_data["actions"][index][1] = num_inputs_types["attributes"]
                                    table_data["data"][row][i+2] = "0.000"
                elif new_type["action_type"] == "Custom":
                    table_data["actions"][index][1] = cus_inputs_types["type"]
                    table_data["data"][row][i+2] = table_data['custom'][cus_inputs_types["type"]][0]

    save(table_data)
    display_table()

def rename_table():
    new_name = input_group("Rename decision table", [
        input("Enter a new name for the table", name="table_name", validate=naming),
    ])
    table_data["table_name"]= new_name["table_name"]
    save(table_data)
    display_table()

# Adds a new action row to the table
def add_action():
    global table_data   # Uses the global value of the table data
    global number2attributes # Uses the global value for number types

    # Prompt user to enter a condition name
    inputs = input_group("Add Action", [
        input("Enter a name for the action:", name="action_name", validate=naming),
        select("Select the type of variable", options=["True/False", "Number", "Custom"], name="action_type"),    # select a conditions
    ])

    if inputs["action_type"] == "Number":
        number_types = list(number2attributes.keys())
        inputs_types = input_group('Select a type:', [
            select('Number type', options=number_types, name='type', onchange=lambda c: input_update('attributes', options=number2attributes[c])),
            select('Attributes', options=number2attributes[number_types[0]], name='attributes'),
        ])
    
    if inputs["action_type"] == "Custom":
        if table_data['custom'] == {}:
            put_text("Create a custom type first")
        else:
            custom_types = list(table_data['custom'].keys())
            cus_inputs_types = input_group('Select a type:', [
                select('Custom type', options=custom_types, name='type'),
            ])

    # Update values in the table data object and conditions list
    table_data["num_actions"] += 1
    position = table_data["num_conditions"] + table_data["num_actions"] + 1
    table_data["data"].insert(position, [" ", inputs["action_name"]])

    # Update rules
    if table_data["num_rules"] != 0:
        for _ in range(table_data["num_rules"]):
            if inputs["action_type"] == "True/False":
                table_data["data"][position].append("False")
            elif inputs["action_type"] == "Number":
                match inputs_types['type']:
                    case "Integer": table_data["data"][position].append(0)
                    case "Range": 
                        if inputs_types["attributes"] == "Inclusive":
                            table_data["data"][position].append('[0,0]')
                        else: table_data["data"][position].append(']0,0[')
                    case "Decimal": 
                        match inputs_types['attributes']:
                            case "1": table_data["data"][position].append('0.0')
                            case "2": table_data["data"][position].append('0.00')
                            case "3": table_data["data"][position].append('0.000')
            elif inputs["action_type"] == "Custom":
                table_data["data"][position].append(table_data['custom'][cus_inputs_types["type"]][0])

    # Add this condition to the global actions list
    if inputs["action_type"] == "True/False":
        table_data['actions'].append([inputs["action_name"], inputs["action_type"]])
    elif inputs["action_type"] == "Number":
        table_data['actions'].append([inputs["action_name"], inputs_types["attributes"]])
    elif inputs["action_type"] == "Custom":
        table_data['actions'].append([inputs["action_name"], cus_inputs_types["type"]])
    
    # Updates the table visual on display
    save(table_data)
    display_table()

# Adds a new rule column to the table
def add_rule():
    global table_data           # Uses the global value of the table data

    if table_data['actions'] == [] and table_data['conditions'] == []:
        put_text("Create a condition or an action first!")
    else:
        # Update values in the table data object and conditions list
        table_data["num_rules"] += 1 
        table_data["headers"].append(table_data["num_rules"])
        for row in table_data["data"]:
            if row[0] != " ":
                    row.append(" ")
            
            # check the type of condition and fill default
            for condition in table_data['conditions']:
                if condition[0] == row[1] and condition[1] == "True/False":
                    row.append("False")
                elif condition[0] == row[1] and condition[1] == "Integer":
                    row.append(0)
                elif condition[0] == row[1] and condition[1] == "Inclusive":
                    row.append('[0,0]')
                elif condition[0] == row[1] and condition[1] == "Exclusive":
                    row.append(']0,0[')
                elif condition[0] == row[1] and condition[1] == "1":
                    row.append('0.0')
                elif condition[0] == row[1] and condition[1] == "2":
                    row.append('0.00')
                elif condition[0] == row[1] and condition[1] == "3":
                    row.append('0.000')
                elif condition[0] == row[1] and condition[1] in list(table_data['custom'].keys()):
                    for custom_type in list(table_data['custom'].keys()):
                        if custom_type == condition[1]: 
                            row.append(table_data['custom'][custom_type][0])

            # check the type of actiona and fill default
            for action in table_data['actions']:
                if action[0] == row[1] and action[1] == "True/False":
                    row.append("False")
                elif action[0] == row[1] and action[1] == "Integer":
                    row.append(0)
                elif action[0] == row[1] and action[1] == "Inclusive":
                    row.append("[0,0]")
                elif action[0] == row[1] and action[1] == "Exclusive":
                    row.append("]0,0[")
                elif action[0] == row[1] and action[1] == "1":
                    row.append('0.0')
                elif action[0] == row[1] and action[1] == "2":
                    row.append('0.00')
                elif action[0] == row[1] and action[1] == "3":
                    row.append('0.000')
                elif action[0] == row[1] and action[1] in list(table_data['custom'].keys()):
                    for custom_type in list(table_data['custom'].keys()):
                        if custom_type == action[1]: 
                            row.append(table_data['custom'][custom_type][0])
        
        
        # Updates the table visual on display
        save(table_data)
        display_table()

def delete_condition(row_index):
    global table_data
    deleted_condition_name = table_data["data"][row_index][1]

    table_data["num_conditions"] -= 1

    # Remove the condition from the conditions list
    table_data['conditions'] = [condition for condition in table_data['conditions'] if condition[0] != deleted_condition_name]

    # Remove the condition from the table data
    del table_data["data"][row_index]

    # Update the UI
    save(table_data)
    display_table()

def delete_action(row_index):
    global table_data
    deleted_action_name = table_data["data"][row_index][1]

    table_data["num_actions"] -= 1

    # Remove the action from the actions list
    table_data['actions'] = [action for action in table_data['actions'] if action[0] != deleted_action_name]

    # Remove the action from the table data
    del table_data["data"][row_index]

    # Update the UI
    save(table_data)
    display_table()

def delete_rule():
    
    global table_data
    
    # prompt which rule(s) to delete
    selected_rules = input("Input rule(s) separated by a comma, (1,2,3):", validate=naming)
    
    selected_list = selected_rules.split(",")
    selected_list.sort(reverse=True)

    for index in selected_list:

        if int(index) > table_data["num_rules"]: return "rule number {} does not exist".format(int(index))
        
        del table_data["headers"][-1]
        row = 0
        for _ in table_data["data"]:
            del table_data["data"][row][int(index)+1]
            
            row += 1

    table_data["num_rules"] -= len(selected_list)

    # Update the UI
    save(table_data)
    display_table()

def add_custom_type():

    inputs = input_group("Add a custom type", [
        input("Enter a name for the custom type:", name="custom_name", validate=naming),
        input("Input type attributes seperated by commas, (a,b,c):", name="custom_type", validate=naming)
    ])
    custom_list = inputs["custom_type"].split(",")
    table_data['custom'][inputs["custom_name"]] = custom_list

    save(table_data)
    display_table()


# Creates a Logical Expression
def logic_expression():

    # Creates an input group pop up to input rule parameters
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

def display_table():
    global table_data   # Uses the global value of the table data

    # table_array is used to pass to the data library put_table function
    table_array = copy.deepcopy(table_data["data"])

    flag = False

    for i in range(len(table_data["data"])):
        if table_data["data"][i][0] == "Conditions":
            continue
        
        if table_data["data"][i][0] == "Actions":
            flag = True
            continue

        if flag == False:
            delete_button = put_button('Delete', onclick=functools.partial(delete_condition, i), small=True, color='info')
            table_array[i].append(delete_button)

        if flag == True:
            delete_button = put_button('Delete', onclick=functools.partial(delete_action, i), small=True, color='info')
            table_array[i].append(delete_button)

    flag = False

    # Convert boolean values to buttons
    for i in range(len(table_data["data"])):
        for j in range(len(table_data["data"][i])):
            if table_array[i][j] == "True" or table_array[i][j] == "False" or table_array[i][j] == "*":
                table_array[i][j] = put_button(table_array[i][j], onclick= functools.partial(toggle_boolean, i, j), color = get_color(table_array[i][j]))
            elif isinstance(table_array[i][j], int):
                table_array[i][j] = put_button(table_array[i][j], onclick= functools.partial(toggle_integer, i, j), color='light')
            elif isinstance(table_array[i][j], str) and table_array[i][j][0] == "[":
                table_array[i][j] = put_button(table_array[i][j], onclick= functools.partial(toggle_range, i, j, "["), color='light')
            elif isinstance(table_array[i][j], str) and table_array[i][j][0] == "]":
                table_array[i][j] = put_button(table_array[i][j], onclick= functools.partial(toggle_range, i, j, "]"), color='light')
            elif isinstance(table_array[i][j], str) and '.' in table_array[i][j]:
                table_array[i][j] = put_button(table_array[i][j], onclick= functools.partial(toggle_decimal, i, j), color='light')
            elif isinstance(table_array[i][j], str) and j > 1 and table_array[i][0] != "Conditions" and table_array[i][0] != "Actions":
                table_array[i][j] = put_button(table_array[i][j], onclick= functools.partial(toggle_custom, i, j), color='light')
            elif isinstance(table_array[i][j], str) and j == 1 and i <= table_data["num_conditions"] and table_array[i][0] != "Conditions" and table_array[i][0] != "Actions":
                table_array[i][j] = put_button(table_array[i][j], onclick= functools.partial(modify_condition, i, j), color='light')
            elif isinstance(table_array[i][j], str) and j == 1 and i > table_data["num_conditions"]+1 and table_array[i][0] != "Conditions" and table_array[i][0] != "Actions":
                table_array[i][j] = put_button(table_array[i][j], onclick= functools.partial(modify_action, i, j), color='light')

    # Update the UI
    clear()
    style(put_text(table_data["table_name"]), "font-weight:bold; font-size:2rem")
    
    put_table(table_array, header=table_data["headers"])

    put_button('Add condition', onclick=add_condition)
    put_button('Add action', onclick=add_action)
    put_button('Add rule', onclick=add_rule)
    put_button('Add a custom type', onclick=add_custom_type)
    put_button('Rename table', onclick=rename_table)
    put_button('Delete a rule', onclick=delete_rule)
    put_button("Close Table", onclick=main)
    # put_button('Add Logical Expression', onclick=logic_expression)

# Toggles the value in the table from where the user interaction came from for booleans
def toggle_boolean(row, column):
    match table_data["data"][row][column]:
        case "False":
            table_data["data"][row][column] = "True"
        case "True":
            table_data["data"][row][column] = "*"
        case "*":
            table_data["data"][row][column] = "False"
        
    save(table_data)
    display_table()

# Toggles the value in the table from where the user interaction came from for integers
def toggle_integer(row, column, ):
    updated_integer = input("Change the value", type=FLOAT)
    table_data["data"][row][column] = int(updated_integer)

    save(table_data)
    display_table()

# Toggles the value in the table from where the user interaction came from for range of values
def toggle_range(row, column, bracket):
    updates = input_group('Update range values', [
        input("Change the first value of the range", type=FLOAT, name="updated_range_a"),
        input("Change the second value of the range", type=FLOAT, name="updated_range_b")
    ])
    if updates["updated_range_a"] > updates["updated_range_b"]: return "the second value must be greater than the first value"
    if bracket == "[":
        table_data["data"][row][column] = "["+str(int(updates["updated_range_a"]))+","+str(int(updates["updated_range_b"]))+"]"
    else: table_data["data"][row][column] = "]"+str(int(updates["updated_range_a"]))+","+str(int(updates["updated_range_b"]))+"["

    save(table_data)
    display_table()

# Toggles the value in the table from where the user interaction came from for decimal values
def toggle_decimal(row, column):
    global table_data
    
    name = table_data["data"][row][1]
    decimal_num = "0"
    for condition in table_data['conditions']:
        if condition[0] == name: 
            decimal_num = condition[1]
            break
    for action in table_data['actions']:
        if action[0] == name:
            decimal_num = action[1]
            break
    
    updated_integer = input("Change the value", type=FLOAT)
    match decimal_num:
        case "1": table_data["data"][row][column] = str("%.1f" % updated_integer)
        case "2": table_data["data"][row][column] = str("%.2f" % updated_integer)
        case "3": table_data["data"][row][column] = str("%.3f" % updated_integer)
    
    save(table_data)
    display_table()

def toggle_custom(row, column):

    name = table_data["data"][row][1]
    attr = "hi"
    for condition in table_data['conditions']:
        if condition[0] == name:
            attr = condition[1]
            break
    for action in table_data['actions']:
        if action[0] == name:
            attr = action[1]
            break
    
    var_list = table_data['custom'][attr]
    
    updated_type = select("Select the value", options=var_list)    # select a conditions
    table_data["data"][row][column] = updated_type

    save(table_data)
    display_table()

def get_color(value):
    if value == "True": return 'success'
    elif value == "False": return 'danger'
    else: return 'warning'

def save(table_data):
    global opened_file
    json_object = json.dumps(table_data, indent=4)
    if (opened_file == None):
        with open(table_data["table_name"]+".json", "w") as outfile:
            outfile.write(json_object)
    else:
        with open(opened_file['filename'], "w") as outfile:
            outfile.write(json_object)

if __name__ == '__main__':
    main()
