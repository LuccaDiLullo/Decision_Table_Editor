from pywebio.input import input, select
from pywebio.output import put_text

# Sample decision table stored as a JSON object
decision_table = {
    "name": "My Decision Table",
    "rules": [
        {"condition": "Condition 1", "action": "Action 1"},
        {"condition": "Condition 2", "action": "Action 2"},
    ],
}

def main():
    while True:
        action = select("Select an action:", ["View Decision Table", "Add Rule", "Exit"])
        
        if action == "View Decision Table":
            put_text(f"Decision Table Name: {decision_table['name']}")
            put_text("Rules:")
            for rule in decision_table['rules']:
                put_text(f"Condition: {rule['condition']}, Action: {rule['action']}")
        
        elif action == "Add Rule":
            condition = input("Enter Condition:")
            action = input("Enter Action:")
            decision_table['rules'].append({"condition": condition, "action": action})

        else:
            break

if __name__ == '__main__':
    main()
