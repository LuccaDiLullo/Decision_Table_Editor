"""
File: main.py
Authors:
  - Julien Lefebvre
  - Justin Randisi
  - Lucca DiLullo
  - Yazan Saleh
Date: February 23, 2024

Description:
  This file serves as the entry point for the decision table application. 
  It provides functions to create and open decision tables. The main 
  function initializes the application and sets up the user interface for 
  creating or opening decision tables.

Usage:
  Run this file to start the decision table application. You can create a 
  new table by clicking the 'Create Table' button and following the prompts, 
  or open an existing table by clicking the 'Open Table' button and 
  selecting a .json file.

"""

import json
from pywebio.input import input, file_upload
from pywebio.output import clear, put_button
from table import Table
from utils import naming_convention

def main():
    clear()
    put_button('Create Table', onclick=create_table)
    put_button('Open Table', onclick=open_table)

def create_table():
    table = Table(callback=main)
    table.data['table_name'] = input("Name this decision table", validate=naming_convention)
    table.save()
    table.display()

def open_table():
    table = Table(callback=main)
    table.file = file_upload("Select .json file to open", accept=".json")
    table.data = json.loads(table.file['content'])
    table.display()

if __name__ == '__main__':
    main()
