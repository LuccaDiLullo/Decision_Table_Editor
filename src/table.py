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

import functools
import json
import ui
from utils import naming_convention, is_range_contained, number_type_attributes
from pywebio.input import input, select, input_group, input_update, checkbox, radio, FLOAT
from pywebio.output import put_button, put_text, popup, close_popup

class Table:
  def __init__(self, callback, file=None):
    self.callback = callback
    self.file = file
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
    self.save()
    self.display()

  def display(self):
    ui.update_table_ui(self)
  
  def save(self):
    json_object = json.dumps(self.data, indent=4)
    if (self.file == None):
      with open(self.data["table_name"]+".json", "w") as outfile:
        outfile.write(json_object)
    else:
      with open(self.file['filename'], "w") as outfile:
        outfile.write(json_object)
  
  def rename(self):
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
    cur_name = self.data['values'][row][column]
    index = 0

    for condition in self.data['conditions']:
      if condition[0] == cur_name: 
        index = self.data['conditions'].index(condition)
        break
    
    inputs = input_group("Modify Condition", [
      select("Would you like to edit the name?", options=["Yes", "No"], name="name", validate=naming_convention),
      select("Would you like to edit the type?", options=["Yes", "No"], name="type", validate=naming_convention)
    ])

    # EDIT BOTH
    if inputs["name"] == "Yes" and inputs["type"] == "Yes": 
      new_vars = input_group("Add Condition", [
        input("Enter a new name for the condition", name="condition_name", validate=naming_convention),
        select("Select a new type", options=["True/False", "Number", "Custom"], name="condition_type"),    # select a conditions
      ])

      if new_vars["condition_type"] == "Number":
        number_types = list(number_type_attributes.keys())
        num_inputs_types = input_group('Select a type:', [
          select('Number type', options=number_types, name='type', onchange=lambda c: input_update('attributes', options=number_type_attributes[c])),
          select('Attributes', options=number_type_attributes[number_types[0]], name='attributes'),
        ])

      if new_vars["condition_type"] == "Custom":
        if self.data['custom'] == {}:
          put_text("Create a custom type first")
        else:
          custom_types = list(self.data['custom'].keys())
          cus_inputs_types = input_group('Select a type:', [
              select('Custom type', options=custom_types, name='type'),
          ])

      self.data['values'][row][column] = new_vars["condition_name"]
      self.data["conditions"][index][0] = new_vars["condition_name"]
      
      # Update rules
      if self.data["num_rules"] != 0:
        for i in range(2, self.data["num_rules"]+2):
          if new_vars["condition_type"] == "True/False":
            self.data["conditions"][index][1] = new_vars["condition_type"]
            self.data['values'][row][i] = "False"
          elif new_vars["condition_type"] == "Number":
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
              self.data["conditions"][index][1] = cus_inputs_types["type"]
              self.data['values'][row][i] = self.data['custom'][cus_inputs_types["type"]][0]
        
    # EDIT NAME ONLY
    elif inputs["name"] == "Yes" and inputs["type"] == "No":
      new_name = input_group("Modify this condition", [
        input("Enter a new name for the condition", name="condition_name", validate=naming_convention),
      ])
      self.data["conditions"][index][0] = new_name["condition_name"]
      self.data['values'][row][column] = new_name["condition_name"]
    
    # EDIT TYPE ONLY
    elif inputs["type"] == "Yes" and inputs["name"] == "No":
      new_type = input_group("Modify this confition", [
        select("Select a new type", options=["True/False", "Number", "Custom"], name="condition_type"),    # select a conditions
      ])

      if new_type["condition_type"] == "Number":
        number_types = list(number_type_attributes.keys())
        num_inputs_types = input_group('Select a type:', [
          select('Number type', options=number_types, name='type', onchange=lambda c: input_update('attributes', options=number_type_attributes[c])),
          select('Attributes', options=number_type_attributes[number_types[0]], name='attributes'),
        ])

      if new_type["condition_type"] == "Custom":
        if self.data['custom'] == {}:
          put_text("Create a custom type first")
        else:
          custom_types = list(self.data['custom'].keys())
          cus_inputs_types = input_group('Select a type:', [
            select('Custom type', options=custom_types, name='type'),
          ])

      # Update rules
      if self.data["num_rules"] != 0:
        for i in range(2, self.data["num_rules"]+2):
          if new_type["condition_type"] == "True/False":
            self.data["conditions"][index][1] = new_type["condition_type"]
            self.data['values'][row][i] = "False"
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
          elif new_type["condition_type"] == "Custom":
              self.data["conditions"][index][1] = cus_inputs_types["type"]
              self.data['values'][row][i] = self.data['custom'][cus_inputs_types["type"]][0]
    
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
    cur_name = self.data['values'][row][column]
    index = 0

    for action in self.data['actions']:
      if action[0] == cur_name: 
        index = self.data['actions'].index(action)
        break
    
    inputs = input_group("Modify Action", [
      select("Would you like to edit the name?", options=["Yes", "No"], name="name", validate=naming_convention),
      select("Would you like to edit the type?", options=["Yes", "No"], name="type", validate=naming_convention)
    ])

    # EDIT BOTH
    if inputs["name"] == "Yes" and inputs["type"] == "Yes": 
      new_vars = input_group("Add Action", [
        input("Enter a new name for the action", name="action_name", validate=naming_convention),
        select("Select a new type", options=["True/False", "Number", "Custom"], name="action_type"),    # select an action
      ])

      if new_vars["action_type"] == "Number":
        number_types = list(number_type_attributes.keys())
        num_inputs_types = input_group('Select a type:', [
          select('Number type', options=number_types, name='type', onchange=lambda c: input_update('attributes', options=number_type_attributes[c])),
          select('Attributes', options=number_type_attributes[number_types[0]], name='attributes'),
        ])

      if new_vars["action_type"] == "Custom":
        if self.data['custom'] == {}:
          put_text("Create a custom type first")
        else:
          custom_types = list(self.data['custom'].keys())
          cus_inputs_types = input_group('Select a type:', [
            select('Custom type', options=custom_types, name='type'),
          ])

      self.data['values'][row][column] = new_vars["action_name"]
      self.data["actions"][index][0] = new_vars["action_name"]
      
      # Update rules
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
        
    # EDIT NAME ONLY
    elif inputs["name"] == "Yes" and inputs["type"] == "No":
      new_name = input_group("Modify this action", [
        input("Enter a new name for the action", name="action_name", validate=naming_convention),
      ])
      self.data["actions"][index][0] = new_name["action_name"]
      self.data['values'][row][column] = new_name["action_name"]
    
    # EDIT TYPE ONLY
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

      # Update rules
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
    index1 = input("Input first rule number to combine:", validate=naming_convention)
    index2 = input("Input second rule number to combine:", validate=naming_convention)

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

      for sublist in self.data["values"]:

        index1 = int(index1)
        index2 = int(index2)

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

      del self.data["headers"][-1]
      row = 0
      for _ in self.data['values']:
        del self.data['values'][row][int(index2)+1]
        row += 1

      self.data["num_rules"] -= 1

    self.update()

  def add_custom_type(self):
    inputs = input_group("Add a custom type", [
      input("Enter a name for the custom type:", name="custom_name", validate=naming_convention),
      input("Input type attributes seperated by commas, (a,b,c):", name="custom_type", validate=naming_convention)
    ])
    custom_list = inputs["custom_type"].split(",")
    self.data['custom'][inputs["custom_name"]] = custom_list

    self.update()

  def identify_warnings(self):
    # Check for unused conditions
    warnings_unused = []
    warnings_redundant = []
    unused_conditions_warnings = []
    if self.data["conditions"] != [] and self.data["num_rules"] != 0:
      row = 1
      for condition in self.data["conditions"]:
        c_name = condition[0]
        c_value = self.data['values'][row][2]

        flag = True
        for i in range(self.data["num_rules"]):
          if self.data['values'][row][i+2] != c_value:
            flag = False
  
        if flag: 
          unused_conditions_warnings.append(row)
          warnings_unused.append(c_name)
        row += 1

    # Check for unused actions
    unused_actions_warnings = []
    if self.data["actions"] != [] and self.data["num_rules"] != 0:
      row = self.data["num_conditions"] + 2
      for action in self.data["actions"]:
        a_name = action[0]
        a_value = self.data['values'][row][2]

        flag = True
        for i in range(self.data["num_rules"]):
          if self.data['values'][row][i+2] != a_value:
            flag = False
            
        if flag: 
          unused_actions_warnings.append(row)
          warnings_unused.append(a_name)
        row += 1
    
    # Check for redundant rules
    redundant_rules = []
    flags = [0] * self.data["num_rules"]
    if self.data["conditions"] != [] and self.data["actions"] != []:
      if self.data["num_rules"] != 0:
        for rule_1 in range(self.data["num_rules"]):
          for rule_2 in range(rule_1+1, self.data["num_rules"]):
            redundant = True
            hasRange = False
            r1_contained = False
            r2_contained = False
            row = self.data["num_conditions"] + 2
            for _ in self.data["actions"]:
              r1_value = self.data['values'][row][rule_1+2]
              r2_value = self.data['values'][row][rule_2+2]
              row += 1
              if r1_value != r2_value:
                redundant = False
                break
            if not redundant: break
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

            if redundant and flags[redundant_rule]==0:
              flags[redundant_rule] = 1
              redundant_rules.append(redundant_rule+1)
              rule_str = f"Rule {redundant_rule+1}"
              warnings_redundant.append(rule_str)

    
    # pop up
    warnings_text = ""
    warning_num = 1
    for warning in warnings_unused:
      warnings_text += "Warning " + str(warning_num) + ": '" + warning + "' is unsused\n" 
      warning_num += 1

    for warning in warnings_redundant:
      warnings_text += "Warning " + str(warning_num) + ": '" + warning + "' is redundant\n" 
      warning_num += 1
    
    if warnings_unused != [] or warnings_redundant != []:
      popup("Identified Warnings", [
        put_text(warnings_text),
        put_button("Fix warnings", functools.partial(self.optimize_table, 
                                                     unused_conditions_warnings, 
                                                     unused_actions_warnings,
                                                     redundant_rules))
      ])
    else:
      popup("No warnings detected, the table is fully optimized!")

  def optimize_table(self, unused_conditions_list, unused_actions_list, redundant_rules_list):
    unused_actions_list.reverse()
    unused_conditions_list.reverse()
    
    for warning in unused_actions_list:
      self.remove_action(warning)
    for warning in unused_conditions_list:
      self.remove_condition(warning)
    for rule in redundant_rules_list:
      self.remove_rule(manual=False, ruleID=rule)

    self.update()
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

  # Toggles the value in the table from where the user interaction came from for integers
  def toggle_integer(self, row, column):
    updated_integer = input("Change the value", type=FLOAT)
    self.data['values'][row][column] = int(updated_integer)
    self.update()

  # Toggles the value in the table from where the user interaction came from for range of values
  def toggle_range(self, row, column, bracket):
    updates = input_group('Update range values', [
      input("Change the first value of the range", type=FLOAT, name="updated_range_a"),
      input("Change the second value of the range", type=FLOAT, name="updated_range_b")
    ])
    if updates["updated_range_a"] > updates["updated_range_b"]:
      return "the second value must be greater than the first value"
    if bracket == "[":
      self.data['values'][row][column] = "["+str(int(updates["updated_range_a"]))+","+str(int(updates["updated_range_b"]))+"]"
    else: 
      self.data['values'][row][column] = "]"+str(int(updates["updated_range_a"]))+","+str(int(updates["updated_range_b"]))+"["

    self.update()

  # Toggles the value in the table from where the user interaction came from for decimal values
  def toggle_decimal(self, row, column):
    name = self.data['values'][row][1]
    decimal_num = "0"
    for condition in self.data['conditions']:
      if condition[0] == name: 
        decimal_num = condition[1]
        break
    for action in self.data['actions']:
      if action[0] == name:
        decimal_num = action[1]
        break
    
    updated_integer = input("Change the value", type=FLOAT)
    match decimal_num:
      case "1": self.data['values'][row][column] = str("%.1f" % updated_integer)
      case "2": self.data['values'][row][column] = str("%.2f" % updated_integer)
      case "3": self.data['values'][row][column] = str("%.3f" % updated_integer)
    
    self.update()

  def toggle_custom(self, row, column):
    name = self.data['values'][row][1]
    attr = "hi"
    for condition in self.data['conditions']:
      if condition[0] == name:
        attr = condition[1]
        break
    for action in self.data['actions']:
      if action[0] == name:
        attr = action[1]
        break
    
    var_list = self.data['custom'][attr]
    
    updated_type = select("Select the value", options=var_list)    # select a conditions
    self.data['values'][row][column] = updated_type

    self.update()
