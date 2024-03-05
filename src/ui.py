"""
File: ui.py
Authors:
  - Julien Lefebvre
  - Justin Randisi
  - Lucca DiLullo
  - Yazan Saleh
Date: February 23, 2024

Description:
  The file contains the user interface (UI) functions for displaying and 
  interacting with tables. Whenever a table is updated, the 
  update_table_ui function is called and updates the display accordingly.

"""

import copy
import functools
from pywebio.output import clear, put_button, put_text, put_table, style
from utils import bool_to_color


def update_table_ui(table):
  table_values = copy.deepcopy(table.data['values'])

  table_values = put_delete_buttons(table, table_values)

  table_values = put_value_toggles(table, table_values)

  clear()
  style(put_text(table.data["table_name"]), "font-weight:bold; font-size:2rem")
  
  put_table(table_values, header=table.data["headers"])

  put_button('Add condition', onclick=table.add_condition)
  put_button('Add action', onclick=table.add_action)
  put_button('Add rule', onclick=table.add_rule)
  put_button('Add a custom type', onclick=table.add_custom_type)
  put_button('Rename table', onclick=table.rename)
  put_button('Delete a rule', onclick=table.remove_rule)
  put_button('Combine rules', onclick=table.combine_rules)
  put_button("Close Table", onclick=table.callback)
  put_button("Optimize Table", onclick=table.identify_warnings)
  return

def put_delete_buttons(table, table_values):
  processing_conditions = True
  num_rows = len(table.data['values'])

  for i in range(num_rows):
    if table.data['values'][i][0] == "Conditions":
      continue
      
    elif table.data['values'][i][0] == "Actions":
      processing_conditions = False
      continue

    if processing_conditions:
      delete_button = put_button('Delete', onclick=functools.partial(table.remove_condition, i), small=True, color='info')
      table_values[i].append(delete_button)

    if not processing_conditions:
      delete_button = put_button('Delete', onclick=functools.partial(table.remove_action, i), small=True, color='info')
      table_values[i].append(delete_button)

  return table_values

def put_value_toggles(table, table_values):
  num_rows = len(table.data['values'])

  for i in range(num_rows):
    num_columns = len(table.data['values'][i])
    for j in range(num_columns):
      value = table_values[i][j]
      if value == "True" or value == "False" or value == "*":
        table_values[i][j] = put_button(value, onclick= functools.partial(table.toggle_boolean, i, j), color = bool_to_color(value))
      elif isinstance(value, int):
        table_values[i][j] = put_button(value, onclick= functools.partial(table.toggle_integer, i, j), color='light')
      elif isinstance(value, str) and value[0] == "[":
        table_values[i][j] = put_button(value, onclick= functools.partial(table.toggle_range, i, j, "["), color='light')
      elif isinstance(value, str) and value[0] == "]":
        table_values[i][j] = put_button(value, onclick= functools.partial(table.toggle_range, i, j, "]"), color='light')
      elif isinstance(value, str) and '.' in value:
        table_values[i][j] = put_button(value, onclick= functools.partial(table.toggle_decimal, i, j), color='light')
      elif isinstance(value, str) and j > 1 and table_values[i][0] != "Conditions" and table_values[i][0] != "Actions":
        table_values[i][j] = put_button(value, onclick= functools.partial(table.toggle_custom, i, j), color='light')
      elif isinstance(value, str) and j == 1 and i <= table.data["num_conditions"] and table_values[i][0] != "Conditions" and table_values[i][0] != "Actions":
        table_values[i][j] = put_button(value, onclick= functools.partial(table.modify_condition, i, j), color='light')
      elif isinstance(value, str) and j == 1 and i > table.data["num_conditions"]+1 and table_values[i][0] != "Conditions" and table_values[i][0] != "Actions":
        table_values[i][j] = put_button(value, onclick= functools.partial(table.modify_action, i, j), color='light')

  return table_values
