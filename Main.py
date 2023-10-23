from pywebio.input import *
from pywebio.output import *

table = []

def main():
    put_button('Create Table', onclick=create_table)


def create_table():
    global table

    if (table == []):
        table_name = input("How should we name this decision table?")
        put_text(table_name)
        table = [['Options', 'Condition 1', 'Action 1'],
            [1, False, put_text("test")], 
            [2, False, put_text("test")],
            [3, False, put_text("test")],
        ]
        put_table(table)
        put_buttons(['Add condition', 'Add action'], onclick=...)


if __name__ == '__main__':
    main()
            