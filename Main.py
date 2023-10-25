from pywebio.input import *
from pywebio.output import *

table = []
conditions = ["condition1", "condition2", "conditiion3"]
actionss = ["action1", "action2", "action3"]

def main():
    global table

    if (table == []):
        table_name = input("How should we name this decision table?")
        put_text(table_name)
        table = [['Options', '< 21', '> 18', 'Adult', 'Legal drinking age'],
            [1, False, False, put_text(" "), put_scope('')], 
            [2, False, True, put_text(" "), put_text(" ")],
            [3, True, False, put_text(" "), put_text(" ")],
            [4, True, True, put_text(" "), put_text(" ")],
        ]

        put_table(table)
        put_button('Add Rule', onclick=add_rule)

def add_rule():
    
    inputs = input_group("Add Rule", [

        select("If [condition]", options=conditions, name="rule_condition"),
        select("is [boolen]", options=["True", "False"], name="rule_boolean"),
        select("Then [action]", options=actionss, name="rule_action"),
        select("is [decision]", options=["True", "False"], name="rule_decision")

    ])

    put_text("Rule: if {} = {}, then {} = {}".format(
        inputs['rule_condition'], inputs['rule_boolean'], inputs['rule_action'], inputs['rule_decision']))

if __name__ == '__main__':
    main()
            