import json


def new_line():
    print()


def print_update(table, column, value):
    print("UPDATE data SET " + column + " = " + value + " WHERE id = " + table)


def print_transactions(committed_transactions):
    new_line()

    # Não tem transações commitadas
    if not committed_transactions:
        print("Não houve nenhuma alteração no banco")
        return

    # Imprime transações do checkpoint que realizaram ou não o Undo
    for transaction in committed_transactions:
        print("TRANSAÇÃO " + transaction + ": realizou Undo")


def print_json(cursor):
    # Execute the query
    cursor.execute("SELECT * FROM data ORDER BY id")
    tuples = cursor.fetchall()

    # Get the column names
    column_names = [desc[0] for desc in cursor.description]

    # Initialize a dictionary to hold the column data
    column_data = {name: [] for name in column_names}

    # Iterate over the tuples
    for tuple in tuples:
        # Iterate over each column in the tuple
        for i, value in enumerate(tuple):
            # Append the value to the appropriate column in the dictionary
            column_data[column_names[i]].append(value)

    # Convert the dictionary to a JSON string
    json_data = json.dumps({"INITIAL": column_data}, indent=2)

    print(json_data)
