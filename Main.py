from pywebio.input import input, put_button
from pywebio.output import put_text, put_table, put_buttons

table = []


def main():
    put_button('Create Table', onclick=create_table)


def create_table():
    global table

    if not table:
        table_name = input("How should we name this decision table?")
        put_text(table_name)
        table = [
            ['Options', 'Condition 1', 'Action 1'],
            [1, False, put_text("test")],
            [2, False, put_text("test")],
            [3, False, put_text("test")],
        ]
        put_table(table)
        put_buttons(['Add condition', 'Add action'], onclick=...)


if __name__ == '__main__':
    main()
