"""
File: table.py
Authors:
  - Julien Lefebvre
  - Justin Randisi
  - Lucca DiLullo
  - Yazan Saleh
Date: February 23, 2024

Description:
  The table.py file defines a Table class that facilitates the creation and 
  manipulation of decision tables. The file contains methods for adding, 
  modifying, and removing conditions, actions, and rules in the decision 
  table. Also for saving, renaming, and optimizing the table.

"""
# Required libraries and modules
import functools
import json
import ui
from utils import naming_convention, is_range_contained, number_type_attributes
from pywebio.input import input, select, input_group, input_update, checkbox, radio, FLOAT
from pywebio.output import put_button, put_text, popup, close_popup

class Table:
  def __init__(self, callback, file=None):
    # Callback function to execute upon certain actions
    self.callback = callback 
    # File attribute for saving the table, if provided
    self.file = file
     # The data attribute stores all information related to the table, including its name, conditions, actions, and rules
    self.data = {
      "table_name": "My Decision Table",
      "num_conditions": 0,
      "conditions": [],
      "num_actions": 0,
      "actions": [],
      "custom": {},
      "num_rules": 0,
      "headers": ["Rules", " "],
      "values": [["Conditions", " "], ["Actions", " "]]
    }

  def update(self):
    # Save the current state of the table and then display it
    self.save()
    self.display()

  def display(self):
    # Display the table using UI methods defined in ui.py
    ui.update_table_ui(self)
  
  def save(self):
    # Save the current state of the table to a JSON file
    json_object = json.dumps(self.data, indent=4)
    if (self.file == None):
      with open(self.data["table_name"]+".json", "w") as outfile:
        outfile.write(json_object)
    else:
      with open(self.file['filename'], "w") as outfile:
        outfile.write(json_object)
  
  def rename(self):
    # Rename the decision table based on user input
    new_name = input_group("Rename decision table", [
        input("Enter a new name for the table", name="table_name", validate=naming_convention),
    ])
    self.data["table_name"] = new_name["table_name"]
    self.update()

  def add_condition(self):
    # Prompt user to enter a condition name
    inputs = input_group("Add Condition", [
      input("Enter a name for the condition:", name="condition_name", validate=naming_convention),
      select("Select the type of variable", options=["True/False", "Number", "Custom"], name="condition_type"),    # select a conditions
    ])

    if inputs["condition_type"] == "Number":
      number_types = list(number_type_attributes.keys())
      num_inputs_types = input_group('Select a type:', [
        select('Number type', options=number_types, name='type', onchange=lambda c: input_update('attributes', options=number_type_attributes[c])),
        select('Attributes', options=number_type_attributes[number_types[0]], name='attributes'),
      ])

    if inputs["condition_type"] == "Custom":
      if self.data['custom'] == {}:
        put_text("Create a custom type first")
      else:
        custom_types = list(self.data['custom'].keys())
        cus_inputs_types = input_group('Select a type:', [
          select('Custom type', options=custom_types, name='type'),
        ])

    # Update values in the table data object and conditions list
    self.data["num_conditions"] += 1
    position = self.data["num_conditions"]
    self.data['values'].insert(position, [" ", inputs["condition_name"]])

    # Update rules
    if self.data["num_rules"] != 0:
      for _ in range(self.data["num_rules"]):
        if inputs["condition_type"] == "True/False":
          self.data['values'][position].append("False")
        elif inputs["condition_type"] == "Number":
          match num_inputs_types["type"]:
            case "Integer": self.data['values'][position].append(0)
            case "Range": 
              if num_inputs_types['attributes'] == "Inclusive":
                self.data['values'][position].append('[0,0]')
              else: self.data['values'][position].append(']0,0[')
            case "Decimal": 
              match num_inputs_types['attributes']:
                case "1": self.data['values'][position].append('0.0')
                case "2": self.data['values'][position].append('0.00')
                case "3": self.data['values'][position].append('0.000')
        elif inputs["condition_type"] == "Custom":
          self.data['values'][position].append(self.data['custom'][cus_inputs_types["type"]][0])
            
    # Add this condition to the global conditions list
    if inputs["condition_type"] == "True/False":
      self.data['conditions'].append([inputs["condition_name"], inputs["condition_type"]])
    elif inputs["condition_type"] == "Number": 
      self.data['conditions'].append([inputs["condition_name"], num_inputs_types["attributes"]])
    elif inputs["condition_type"] == "Custom":
      self.data['conditions'].append([inputs["condition_name"], cus_inputs_types["type"]])
    
    # Updates the table visual on display
    self.update()
  
  def modify_condition(self, row, column):    
    # Identify the current condition name based on the selected table cell
    cur_name = self.data['values'][row][column]
    index = 0

    # Find the index of the current condition within the conditions list
    for condition in self.data['conditions']:
      if condition[0] == cur_name: 
        index = self.data['conditions'].index(condition)
        break
    
    # Prompt the user to decide whether they want to edit the name and/or the type of the condition
    inputs = input_group("Modify Condition", [
      select("Would you like to edit the name?", options=["Yes", "No"], name="name", validate=naming_convention),
      select("Would you like to edit the type?", options=["Yes", "No"], name="type", validate=naming_convention)
    ])

    # If the user decides to edit both the name and the type of the condition
    if inputs["name"] == "Yes" and inputs["type"] == "Yes": 
      new_vars = input_group("Add Condition", [
        input("Enter a new name for the condition", name="condition_name", validate=naming_convention),
        select("Select a new type", options=["True/False", "Number", "Custom"], name="condition_type"),    # select a conditions
      ])

      # Handle modifications for a Number type condition
      if new_vars["condition_type"] == "Number":
        number_types = list(number_type_attributes.keys())
        num_inputs_types = input_group('Select a type:', [
          select('Number type', options=number_types, name='type', onchange=lambda c: input_update('attributes', options=number_type_attributes[c])),
          select('Attributes', options=number_type_attributes[number_types[0]], name='attributes'),
        ])

      # Handle modifications for a Custom type condition
      if new_vars["condition_type"] == "Custom":
        if self.data['custom'] == {}:
          put_text("Create a custom type first")
        else:
          custom_types = list(self.data['custom'].keys())
          cus_inputs_types = input_group('Select a type:', [
              select('Custom type', options=custom_types, name='type'),
          ])

      # Update the condition's name in the table values and conditions list
      self.data['values'][row][column] = new_vars["condition_name"]
      self.data["conditions"][index][0] = new_vars["condition_name"]
      
      # Update the condition's type and default values in rules if any rules exist
      if self.data["num_rules"] != 0:
        for i in range(2, self.data["num_rules"]+2):
          if new_vars["condition_type"] == "True/False":
            self.data["conditions"][index][1] = new_vars["condition_type"]
            self.data['values'][row][i] = "False"
          elif new_vars["condition_type"] == "Number":
            # Update based on the selected number type and attributes
            match num_inputs_types["type"]:
              case "Integer": 
                self.data["conditions"][index][1] = num_inputs_types["attributes"]
                self.data['values'][row][i] = 0
              case "Range": 
                if num_inputs_types['attributes'] == "Inclusive":
                    self.data["conditions"][index][1] = num_inputs_types["attributes"]
                    self.data['values'][row][i] = "[0,0]"
                else: 
                    self.data["conditions"][index][1] = num_inputs_types["attributes"]
                    self.data['values'][row][i] = "]0,0["
              case "Decimal": 
                match num_inputs_types['attributes']:
                  case "1": 
                      self.data["conditions"][index][1] = num_inputs_types["attributes"]
                      self.data['values'][row][i] = "0.0"
                  case "2": 
                      self.data["conditions"][index][1] = num_inputs_types["attributes"]
                      self.data['values'][row][i] = "0.00"
                  case "3": 
                      self.data["conditions"][index][1] = num_inputs_types["attributes"]
                      self.data['values'][row][i] = "0.000"
          elif new_vars["condition_type"] == "Custom":
              # Update based on the selected custom type
              self.data["conditions"][index][1] = cus_inputs_types["type"]
              self.data['values'][row][i] = self.data['custom'][cus_inputs_types["type"]][0]
        
    # If the user decides to edit only the name of the condition
    elif inputs["name"] == "Yes" and inputs["type"] == "No":
      new_name = input_group("Modify this condition", [
        input("Enter a new name for the condition", name="condition_name", validate=naming_convention),
      ])
      self.data["conditions"][index][0] = new_name["condition_name"]
      self.data['values'][row][column] = new_name["condition_name"]
    
    # This branch allows modifying only the type of a condition, keeping the name unchanged.
    elif inputs["type"] == "Yes" and inputs["name"] == "No":
      # Gather new type information from the user.
      new_type = input_group("Modify this confition", [
        select("Select a new type", options=["True/False", "Number", "Custom"], name="condition_type"),    # select a conditions
      ])

      # If the new type is Number, prompt for further details regarding number type and attributes.
      if new_type["condition_type"] == "Number":
        number_types = list(number_type_attributes.keys())
        num_inputs_types = input_group('Select a type:', [
          select('Number type', options=number_types, name='type', onchange=lambda c: input_update('attributes', options=number_type_attributes[c])),
          select('Attributes', options=number_type_attributes[number_types[0]], name='attributes'),
        ])

      # If the new type is Custom, allow selection from predefined custom types, prompting to create one if none exist.
      if new_type["condition_type"] == "Custom":
        if self.data['custom'] == {}:
          # Notify user to create a custom type if none exists.
          put_text("Create a custom type first") 
        else:
          # Get custom types from the table's data.
          custom_types = list(self.data['custom'].keys())
          cus_inputs_types = input_group('Select a type:', [
            select('Custom type', options=custom_types, name='type'),
          ])

      # Update rules based on the new type, applying changes to all relevant places in the table's data.
      if self.data["num_rules"] != 0:
        for i in range(2, self.data["num_rules"]+2):
          # Apply updates for True/False conditions.
          if new_type["condition_type"] == "True/False":
            self.data["conditions"][index][1] = new_type["condition_type"]
            self.data['values'][row][i] = "False"
          # Apply updates based on the selected number type and its attributes.
          elif new_type["condition_type"] == "Number":
            match num_inputs_types["type"]:
              case "Integer": 
                self.data["conditions"][index][1] = num_inputs_types["attributes"]
                self.data['values'][row][i] = 0
              case "Range": 
                if num_inputs_types['attributes'] == "Inclusive":
                  self.data["conditions"][index][1] = num_inputs_types["attributes"]
                  self.data['values'][row][i] = "[0,0]"
                else: 
                  self.data["conditions"][index][1] = num_inputs_types["attributes"]
                  self.data['values'][row][i] = "]0,0["
              case "Decimal": 
                match num_inputs_types['attributes']:
                  case "1": 
                    self.data["conditions"][index][1] = num_inputs_types["attributes"]
                    self.data['values'][row][i] = "0.0"
                  case "2": 
                    self.data["conditions"][index][1] = num_inputs_types["attributes"]
                    self.data['values'][row][i] = "0.00"
                  case "3": 
                    self.data["conditions"][index][1] = num_inputs_types["attributes"]
                    self.data['values'][row][i] = "0.000"
          # Apply updates for Custom conditions.
          elif new_type["condition_type"] == "Custom":
              self.data["conditions"][index][1] = cus_inputs_types["type"]
              self.data['values'][row][i] = self.data['custom'][cus_inputs_types["type"]][0]
    
    # Ensure the table UI is updated to reflect these changes.
    self.update()

  def remove_condition(self, row_index):
    condition_to_remove = self.data['values'][row_index][1]
    self.data["num_conditions"] -= 1
    # Remove the condition from the conditions list
    self.data['conditions'] = [condition for condition in self.data['conditions'] if condition[0] != condition_to_remove]
    # Remove the condition from the table data
    del self.data['values'][row_index]
    self.update()
  
  def add_action(self):
    # Prompt user to enter a condition name
    inputs = input_group("Add Action", [
      input("Enter a name for the action:", name="action_name", validate=naming_convention),
      select("Select the type of variable", options=["True/False", "Number", "Custom"], name="action_type"),    # select a conditions
    ])

    if inputs["action_type"] == "Number":
      number_types = list(number_type_attributes.keys())
      inputs_types = input_group('Select a type:', [
        select('Number type', options=number_types, name='type', onchange=lambda c: input_update('attributes', options=number_type_attributes[c])),
        select('Attributes', options=number_type_attributes[number_types[0]], name='attributes'),
      ])
    
    if inputs["action_type"] == "Custom":
      if self.data['custom'] == {}:
        put_text("Create a custom type first")
      else:
        custom_types = list(self.data['custom'].keys())
        cus_inputs_types = input_group('Select a type:', [
          select('Custom type', options=custom_types, name='type'),
        ])

    # Update values in the table data object and conditions list
    self.data["num_actions"] += 1
    position = self.data["num_conditions"] + self.data["num_actions"] + 1
    self.data['values'].insert(position, [" ", inputs["action_name"]])

    # Update rules
    if self.data["num_rules"] != 0:
      for _ in range(self.data["num_rules"]):
        if inputs["action_type"] == "True/False":
            self.data['values'][position].append("False")
        elif inputs["action_type"] == "Number":
          match inputs_types['type']:
            case "Integer": self.data['values'][position].append(0)
            case "Range": 
              if inputs_types["attributes"] == "Inclusive":
                self.data['values'][position].append('[0,0]')
              else: self.data['values'][position].append(']0,0[')
            case "Decimal": 
              match inputs_types['attributes']:
                case "1": self.data['values'][position].append('0.0')
                case "2": self.data['values'][position].append('0.00')
                case "3": self.data['values'][position].append('0.000')
        elif inputs["action_type"] == "Custom":
          self.data['values'][position].append(self.data['custom'][cus_inputs_types["type"]][0])

    # Add this condition to the global actions list
    if inputs["action_type"] == "True/False":
      self.data['actions'].append([inputs["action_name"], inputs["action_type"]])
    elif inputs["action_type"] == "Number":
      self.data['actions'].append([inputs["action_name"], inputs_types["attributes"]])
    elif inputs["action_type"] == "Custom":
      self.data['actions'].append([inputs["action_name"], cus_inputs_types["type"]])
    
    # Updates the table visual on display
    self.update()

  def modify_action(self, row, column):
    # Identify the current name of the action to be modified
    cur_name = self.data['values'][row][column]
    index = 0

    # Find the action's index within the actions list
    for action in self.data['actions']:
      if action[0] == cur_name: 
        index = self.data['actions'].index(action)
        break
    
    # Prompt the user to decide whether to edit the name and/or type of the action
    inputs = input_group("Modify Action", [
      select("Would you like to edit the name?", options=["Yes", "No"], name="name", validate=naming_convention),
      select("Would you like to edit the type?", options=["Yes", "No"], name="type", validate=naming_convention)
    ])

    # If the user chooses to edit both the name and type
    if inputs["name"] == "Yes" and inputs["type"] == "Yes": 
      # Collect new name and type for the action
      new_vars = input_group("Add Action", [
        input("Enter a new name for the action", name="action_name", validate=naming_convention),
        select("Select a new type", options=["True/False", "Number", "Custom"], name="action_type"),    # select an action
      ])

      # Handle the case where the new type is "Number"
      if new_vars["action_type"] == "Number":
        number_types = list(number_type_attributes.keys())
        num_inputs_types = input_group('Select a type:', [
          select('Number type', options=number_types, name='type', onchange=lambda c: input_update('attributes', options=number_type_attributes[c])),
          select('Attributes', options=number_type_attributes[number_types[0]], name='attributes'),
        ])

      # Handle the case where the new type is "Custom"
      if new_vars["action_type"] == "Custom":
        if self.data['custom'] == {}:
          put_text("Create a custom type first")
        else:
          custom_types = list(self.data['custom'].keys())
          cus_inputs_types = input_group('Select a type:', [
            select('Custom type', options=custom_types, name='type'),
          ])

      # Update the action name and type in the data structure
      self.data['values'][row][column] = new_vars["action_name"]
      self.data["actions"][index][0] = new_vars["action_name"]
      
      # Update corresponding rules with the new action details
      if self.data["num_rules"] != 0:
        for i in range(self.data["num_rules"]):
          if new_vars["action_type"] == "True/False":
            self.data["actions"][index][1] = new_vars["action_type"]
            self.data['values'][row][i+2] = "False"
          elif new_vars["action_type"] == "Number":
            match num_inputs_types["type"]:
              case "Integer": 
                self.data["actions"][index][1] = num_inputs_types["attributes"]
                self.data['values'][row][i+2] = 0
              case "Range": 
                if num_inputs_types['attributes'] == "Inclusive":
                  self.data["actions"][index][1] = num_inputs_types["attributes"]
                  self.data['values'][row][i+2] = "[0,0]"
                else: 
                  self.data["actions"][index][1] = num_inputs_types["attributes"]
                  self.data['values'][row][i+2] = "]0,0["
              case "Decimal": 
                match num_inputs_types['attributes']:
                  case "1": 
                    self.data["actions"][index][1] = num_inputs_types["attributes"]
                    self.data['values'][row][i+2] = "0.0"
                  case "2": 
                    self.data["actions"][index][1] = num_inputs_types["attributes"]
                    self.data['values'][row][i+2] = "0.00"
                  case "3": 
                    self.data["actions"][index][1] = num_inputs_types["attributes"]
                    self.data['values'][row][i+2] = "0.000"
          elif new_vars["action_type"] == "Custom":
              self.data["actions"][index][1] = cus_inputs_types["type"]
              self.data['values'][row][i+2] = self.data['custom'][cus_inputs_types["type"]][0]
        
    # If the user chooses to only edit the name of the action
    elif inputs["name"] == "Yes" and inputs["type"] == "No":
      new_name = input_group("Modify this action", [
        input("Enter a new name for the action", name="action_name", validate=naming_convention),
      ])
      # Update the action name in the data structure
      self.data["actions"][index][0] = new_name["action_name"]
      self.data['values'][row][column] = new_name["action_name"]
    
    # If the user chooses to only edit the type of the action
    elif inputs["type"] == "Yes" and inputs["name"] == "No":
      new_type = input_group("Modify this action", [
        select("Select a new type", options=["True/False", "Number", "Custom"], name="action_type"),    # select an action
      ])

      if new_type["action_type"] == "Number":
        number_types = list(number_type_attributes.keys())
        num_inputs_types = input_group('Select a type:', [
          select('Number type', options=number_types, name='type', onchange=lambda c: input_update('attributes', options=number_type_attributes[c])),
          select('Attributes', options=number_type_attributes[number_types[0]], name='attributes'),
        ])

      if new_type["action_type"] == "Custom":
        if self.data['custom'] == {}:
          put_text("Create a custom type first")
        else:
          custom_types = list(self.data['custom'].keys())
          cus_inputs_types = input_group('Select a type:', [
            select('Custom type', options=custom_types, name='type'),
          ])

      # Update corresponding rules with the new action details
      if self.data["num_rules"] != 0:
        for i in range(self.data["num_rules"]):
          if new_type["action_type"] == "True/False":
            self.data["actions"][index][1] = new_type["action_type"]
            self.data['values'][row][i+2] = "False"
          elif new_type["action_type"] == "Number":
            match num_inputs_types["type"]:
              case "Integer": 
                self.data["actions"][index][1] = num_inputs_types["attributes"]
                self.data['values'][row][i+2] = 0
              case "Range": 
                if num_inputs_types['attributes'] == "Inclusive":
                  self.data["actions"][index][1] = num_inputs_types["attributes"]
                  self.data['values'][row][i+2] = "[0,0]"
                else: 
                  self.data["actions"][index][1] = num_inputs_types["attributes"]
                  self.data['values'][row][i+2] = "]0,0["
              case "Decimal": 
                match num_inputs_types['attributes']:
                  case "1": 
                    self.data["actions"][index][1] = num_inputs_types["attributes"]
                    self.data['values'][row][i+2] = "0.0"
                  case "2": 
                    self.data["actions"][index][1] = num_inputs_types["attributes"]
                    self.data['values'][row][i+2] = "0.00"
                  case "3": 
                    self.data["actions"][index][1] = num_inputs_types["attributes"]
                    self.data['values'][row][i+2] = "0.000"
          elif new_type["action_type"] == "Custom":
              self.data["actions"][index][1] = cus_inputs_types["type"]
              self.data['values'][row][i+2] = self.data['custom'][cus_inputs_types["type"]][0]

    self.update()
  
  def remove_action(self, row_index):
    action_to_remove = self.data['values'][row_index][1]
    self.data["num_actions"] -= 1
    # Remove the action from the actions list
    self.data['actions'] = [action for action in self.data['actions'] if action[0] != action_to_remove]
    # Remove the action from the table data
    del self.data['values'][row_index]
    self.update()
  
  def add_rule(self):

    if self.data['actions'] == [] and self.data['conditions'] == []:
      put_text("Create a condition or an action first!")
    else:
      # Update values in the table data object and conditions list
      self.data["num_rules"] += 1 
      self.data["headers"].append(self.data["num_rules"])
      for row in self.data['values']:
        if row[0] != " ":
          row.append(" ")
        
        # check the type of condition and fill default
        for condition in self.data['conditions']:
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
          elif condition[0] == row[1] and condition[1] in list(self.data['custom'].keys()):
            for custom_type in list(self.data['custom'].keys()):
              if custom_type == condition[1]: 
                row.append(self.data['custom'][custom_type][0])

        # check the type of actiona and fill default
        for action in self.data['actions']:
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
          elif action[0] == row[1] and action[1] in list(self.data['custom'].keys()):
            for custom_type in list(self.data['custom'].keys()):
              if custom_type == action[1]: 
                row.append(self.data['custom'][custom_type][0])
        
      self.update()
  
  def remove_rule(self, manual=True, ruleID=None):
    if manual or ruleID == None: 
      # prompt which rule(s) to delete
      inputs = input_group("Add Condition", [
        checkbox("", name="incomplete", options=['Delete all incomplete rules']),
        input("Input rule number to delete:", name="rule_index"),
      ])
      
      index = inputs["rule_index"]

      # Check for incomplete rules
      incomplete_rules = []
      if inputs["incomplete"]: 
        for rule in range(0,self.data['num_rules']):
          row_index = 0
          for row in self.data['values']:
            # if cell equals default, it is incomplete?
            if self.data['values'][row_index][0] != 'Conditions' and self.data['values'][row_index][0] != 'Actions':
              cell_value = self.data['values'][row_index][rule+2]
              cell_name = self.data['values'][row_index][1]
              cell_type = ''
              for condition in self.data['conditions']:
                if condition[0] == cell_name:
                  cell_type = condition[1]
              for action in self.data["actions"]:
                if action[0] == cell_name:
                  cell_type = action[1]

              if (cell_type == "True/False" and cell_value == 'False') or (cell_type == "Integer" and cell_value == 0) or (cell_type == "Inclusive" and cell_value == '[0,0]') or (cell_type == "Exclusive" and cell_value == ']0,0[') or (cell_type == "1" and cell_value == '0.0') or (cell_type == "2" and cell_value == '0.00') or (cell_type == "3" and cell_value == '0.000'):
                incomplete_rules.append(rule+1)
            
            row_index += 1
        
        # Delete incomplete rules
        if incomplete_rules != []:
          incomplete_rules.reverse()
          for i in incomplete_rules:
            self.remove_rule(manual=False, ruleID=i)
        else:
          put_text("All rules are complete")
        
        return 0

    else:
      index = ruleID

    if isinstance(int(index), int):
      if int(index) > self.data["num_rules"]: 
        return "rule number {} does not exist".format(int(index))

      if int(index) <= 0:
        return "Invalid index"
      
      del self.data["headers"][-1]
      row = 0
      for _ in self.data['values']:
        del self.data['values'][row][int(index)+1]
        row += 1

      self.data["num_rules"] -= 1

    self.update()
    return 0

  def combine_rules(self):
    # Prompt the user to input two rule numbers that they wish to combine.
    index1 = input("Input first rule number to combine:", validate=naming_convention)
    index2 = input("Input second rule number to combine:", validate=naming_convention)

    # Validate the rule numbers to ensure they are within the valid range and not identical.
    if isinstance(int(index1), int) and isinstance(int(index2), int):
      if int(index1) > self.data["num_rules"]: 
        return "rule number {} does not exist".format(int(index1))

      if int(index2) > self.data["num_rules"]: 
        return "rule number {} does not exist".format(int(index2))

      if int(index1) == int(index2):
        return "Can't combine a rule with itself"

      if int(index1) <= 0:
        return "Invalid index"

      if int(index2) <= 0:
        return "Invalid index"

      # Iterate through the values in the decision table to combine the specified rules.
      for sublist in self.data["values"]:

        index1 = int(index1)
        index2 = int(index2)
        # Logic to combine the rules based on their conditions and actions.
        if sublist[1+index1] == "False" or sublist[1+index1] == "True" or sublist[1+index1] == "*":
          if sublist[1+index1] == "*":
            sublist[1+index1] = sublist[1+index2]
          if sublist[1+index1] == "False":
            sublist[1+index1] = "False"
          if sublist[1+index1] == "True":
            if sublist[1+index2] == "True" or sublist[1+index2] == "*":
              sublist[1+index1] = "True"
            else:
               sublist[1+index1] = "False"

      # Remove the second rule from the headers to reflect its combination into the first rule.
      del self.data["headers"][-1]
      row = 0
      # Remove the second rule's column from each row in the values list.
      for _ in self.data['values']:
        del self.data['values'][row][int(index2)+1]
        row += 1

      # Decrement the number of rules to reflect the combination.
      self.data["num_rules"] -= 1

    self.update()

  def add_custom_type(self):
    # Prompt the user to define a new custom type by specifying a name and its attributes.
    inputs = input_group("Add a custom type", [
      input("Enter a name for the custom type:", name="custom_name", validate=naming_convention),
      input("Input type attributes seperated by commas, (a,b,c):", name="custom_type", validate=naming_convention)
    ])
    # Split the provided attributes string into a list by commas, allowing for multiple attributes.
    custom_list = inputs["custom_type"].split(",")
    # Add the new custom type and its attributes to the 'custom' dictionary within the table's data structure.
    self.data['custom'][inputs["custom_name"]] = custom_list

    self.update()

  def identify_warnings(self):
    # Initialize lists to keep track of unused and redundant items.
    warnings_unused = []
    warnings_redundant = []
    unused_conditions_warnings = []

    # Check each condition to see if it's used in any rule. If not, mark it as unused.
    if self.data["conditions"] != [] and self.data["num_rules"] != 0:
      # Start from the first condition's row
      row = 1
      for condition in self.data["conditions"]:
        c_name = condition[0]
        c_value = self.data['values'][row][2]

        # Flag to mark the condition as unused initially
        flag = True
        for i in range(self.data["num_rules"]):
          # If any rule uses the condition differently, it's considered used.
          if self.data['values'][row][i+2] != c_value:
            flag = False
  
        # If the condition is unused, add it to the warnings list.
        if flag: 
          unused_conditions_warnings.append(row)
          warnings_unused.append(c_name)
        row += 1

    # Similar check for actions to identify unused actions.
    unused_actions_warnings = []
    if self.data["actions"] != [] and self.data["num_rules"] != 0:
      row = self.data["num_conditions"] + 2
      for action in self.data["actions"]:
        a_name = action[0]
        a_value = self.data['values'][row][2]

        # Flag for unused actions
        flag = True
        for i in range(self.data["num_rules"]):
          if self.data['values'][row][i+2] != a_value:
            flag = False
            
        if flag: 
          unused_actions_warnings.append(row)
          warnings_unused.append(a_name)
        row += 1
    
    # Check for redundant rules, i.e., rules that could be combined without loss of functionality.
    redundant_rules = []
    # Flags to avoid double counting
    flags = [0] * self.data["num_rules"]
    if self.data["conditions"] != [] and self.data["actions"] != []:
      if self.data["num_rules"] != 0:
        for rule_1 in range(self.data["num_rules"]):
          for rule_2 in range(rule_1+1, self.data["num_rules"]):
            redundant = True
            hasRange = False
            r1_contained = False
            r2_contained = False
            # Compare the actions of the two rules.
            row = self.data["num_conditions"] + 2
            for _ in self.data["actions"]:
              r1_value = self.data['values'][row][rule_1+2]
              r2_value = self.data['values'][row][rule_2+2]
              row += 1
              if r1_value != r2_value:
                redundant = False
                break
            if not redundant: break
            # Compare the conditions of the two rules.
            row = 1
            for condition in self.data["conditions"]:
              cond_type = condition[1]
              r1_value = self.data['values'][row][rule_1+2]
              r2_value = self.data['values'][row][rule_2+2]
              row += 1
              if cond_type == "Inclusive" or cond_type == "Exclusive":
                hasRange = True
                if r1_value != r2_value:
                  if is_range_contained(r2_value, r1_value):
                    r2_contained = True
                  elif is_range_contained(r1_value, r2_value):
                    r1_contained = True
                  else:
                    redundant = False
                    break
              else:
                if r1_value != r2_value:
                  redundant = False
                  break      

            if r2_contained and not r1_contained:
              redundant_rule = rule_2
            elif r1_contained and not r2_contained:
              redundant_rule = rule_1
            else:
              redundant_rule = rule_2
              if hasRange: redundant = False

            # Decide which rule is redundant based on containment.
            if redundant and flags[redundant_rule]==0:
              flags[redundant_rule] = 1
              redundant_rules.append(redundant_rule+1)
              rule_str = f"Rule {redundant_rule+1}"
              warnings_redundant.append(rule_str)

    
    # Display warnings for unused items and redundant rules.
    warnings_text = ""
    warning_num = 1
    for warning in warnings_unused:
      warnings_text += "Warning " + str(warning_num) + ": '" + warning + "' is unsused\n" 
      warning_num += 1

    for warning in warnings_redundant:
      warnings_text += "Warning " + str(warning_num) + ": '" + warning + "' is redundant\n" 
      warning_num += 1
    
    # If there are any warnings, display them in a pop up
    if warnings_unused != [] or warnings_redundant != []:
      popup("Identified Warnings", [
        put_text(warnings_text),
        put_button("Fix warnings", functools.partial(self.optimize_table, 
                                                     unused_conditions_warnings, 
                                                     unused_actions_warnings,
                                                     redundant_rules))
      ])
    else:
      # Notify the user that no warnings were detected and the table is considered optimized.
      popup("No warnings detected, the table is fully optimized!")

  def optimize_table(self, unused_conditions_list, unused_actions_list, redundant_rules_list):
    # Reverse the lists to ensure that removing items doesn't shift the indices of yet-to-be-processed items.
    unused_actions_list.reverse()
    unused_conditions_list.reverse()
    
    # Remove unused actions. By iterating over the reversed list, we ensure that deleting one action
    # doesn't affect the indices of the remaining actions to be deleted
    for warning in unused_actions_list:
      self.remove_action(warning)
    
    # Similarly, remove unused conditions. This step helps in cleaning up the decision table,
    # making it more efficient and easier to manage.
    for warning in unused_conditions_list:
      self.remove_condition(warning)
    
    # Remove redundant rules identified in the decision table. This operation further optimizes
    # the table by combining or eliminating rules that do not contribute to the decision-making process.
    for rule in redundant_rules_list:
      self.remove_rule(manual=False, ruleID=rule)

    self.update()
    # Notify the user that the optimization process is complete and close the popup.
    put_text("optimization complete")
    close_popup()

  # Toggles the value in the table from where the user interaction came from for booleans
  def toggle_boolean(self, row, column):
    match self.data['values'][row][column]:
      case "False":
        self.data['values'][row][column] = "True"
      case "True":
        self.data['values'][row][column] = "*"
      case "*":
        self.data['values'][row][column] = "False"
        
    self.update()

 
  def toggle_integer(self, row, column):
     # Toggles the value in the table from where the user interaction came from for integers
    updated_integer = input("Change the value", type=FLOAT)
    self.data['values'][row][column] = int(updated_integer)
    self.update()


  def toggle_range(self, row, column, bracket):
    # This function allows for the editing of range values in the decision table.
    # It prompts the user to input new start and end values for a specified range.
    updates = input_group('Update range values', [
      input("Change the first value of the range", type=FLOAT, name="updated_range_a"),
      input("Change the second value of the range", type=FLOAT, name="updated_range_b")
    ])
    # Validate the input to ensure the start of the range is less than the end.
    if updates["updated_range_a"] > updates["updated_range_b"]:
      return "the second value must be greater than the first value"
    # Depending on the type of bracket provided ('[' for inclusive, ']' for exclusive),
    # format the range string accordingly.
    if bracket == "[":
      # For inclusive ranges, both end values are included in the range.
      self.data['values'][row][column] = "["+str(int(updates["updated_range_a"]))+","+str(int(updates["updated_range_b"]))+"]"
    else: 
      # For exclusive ranges, both end values are excluded from the range.
      self.data['values'][row][column] = "]"+str(int(updates["updated_range_a"]))+","+str(int(updates["updated_range_b"]))+"["

    self.update()

  
  def toggle_decimal(self, row, column):
    # Identify the name of the condition or action to determine the type of decimal precision required.
    name = self.data['values'][row][1]
    decimal_num = "0"
    # Look up the corresponding condition or action in the table data to find its decimal precision setting.
    for condition in self.data['conditions']:
      if condition[0] == name: 
        decimal_num = condition[1]
        break
    for action in self.data['actions']:
      if action[0] == name:
        decimal_num = action[1]
        break
    
    # Prompt the user to input a new value for the decimal, ensuring it's treated as a float for precision.
    updated_integer = input("Change the value", type=FLOAT)

    # Update the value in the table based on the specified precision ('1', '2', or '3' decimals).
    match decimal_num:
      case "1": self.data['values'][row][column] = str("%.1f" % updated_integer)
      case "2": self.data['values'][row][column] = str("%.2f" % updated_integer)
      case "3": self.data['values'][row][column] = str("%.3f" % updated_integer)
    
    self.update()

  def toggle_custom(self, row, column):
    # Retrieve the name of the condition or action from the specified row.
    name = self.data['values'][row][1]
    attr = "hi"
    # Search for the condition or action in the table's data to find its associated custom type attribute.
    for condition in self.data['conditions']:
      if condition[0] == name:
        attr = condition[1]
        break
    for action in self.data['actions']:
      if action[0] == name:
        attr = action[1]
        break
    
    # Retrieve the list of options for the custom type.
    var_list = self.data['custom'][attr]
    
    # Prompt the user to select a new value for the custom attribute from the available options.
    updated_type = select("Select the value", options=var_list)    # select a conditions
    
    # Update the cell in the decision table with the newly selected custom value.
    self.data['values'][row][column] = updated_type

    # Refresh the table UI to reflect the change.
    self.update()
