"""
File: main.py
Authors:
  - Julien Lefebvre
  - Justin Randisi
  - Lucca DiLullo
  - Yazan Saleh
Date: March 26, 2024

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
# Required libraries and modules
import json
from pywebio.input import input, file_upload
from pywebio.output import clear, put_button
from table import Table
from utils import naming_convention

def main():
    # Clears the current output in the web page and displays buttons for creating or opening a table.
    clear()

    # Button to create a new decision table.
    put_button('Create Table', onclick=create_table)

    # Button to open an existing decision table.
    put_button('Open Table', onclick=open_table)


def create_table():
    # Function to create a new decision table.

    # Initializes a new Table object with 'main' as the callback function.
    table = Table(callback=main)

    # Prompts the user to name the new decision table, ensuring the name adheres to a naming convention.
    table.data['table_name'] = input("Name this decision table", validate=naming_convention)

    # Saves the newly created table to a file.
    table.save()

    # Displays the newly created table.
    table.display()


def open_table():
    # Function to open an existing decision table.

    # Initializes a new Table object with 'main' as the callback function.
    table = Table(callback=main)

    # Prompts the user to upload a .json file representing a decision table.
    table.file = file_upload("Select .json file to open", accept=".json")

    # Loads the decision table data from the uploaded file's content.
    table.data = json.loads(table.file['content'])

    # Displays the decision table loaded from the file.
    table.display()


if __name__ == '__main__':
    main()
