"""
File: utils.py
Authors:
  - Julien Lefebvre
  - Justin Randisi
  - Lucca DiLullo
  - Yazan Saleh
Date: February 22, 2024

Description:
  This file provides utility functions to support various aspects of UI 
  or table manipulations in the application.

Usage:
  From the other files of the source code, import utils or selected 
  functions from utils when needed.

"""

# Function to pass as validation in UI inputs enforcing naming length limits
def naming_convention(name):
  if len(name) < 1 or len(name) > 32:
    return "Name must be between 1 than 32 characters"
  
# Function to convert a boolean value into a corresponding color label
# Color labels from PyWebIO library:
# - success: Green
# - danger: Red
# - warning: Yellow
def bool_to_color(value):
  if value == "True":
    return 'success'
  elif value == "False":
    return 'danger'
  else:
    return 'warning'
  
# Lookup dictionary for different number types as keys. 
# Values are lists of attributes related to the corresponding number type
number_type_attributes = {
  'Integer': ['Integer'],
  'Range': ['Inclusive', 'Exclusive'],
  'Decimal': ["1", "2", "3"]
}