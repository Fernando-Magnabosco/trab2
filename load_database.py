import json


def create_table(cursor, columns):
    cursor.execute("DROP TABLE IF EXISTS data;")
    # Create a string of column definitions
    column_defs = ", ".join([f"{column} integer NOT NULL" for column in columns])

    cursor.execute(
        f"""
                CREATE TABLE data (
                    {column_defs}
                );
                """
    )


def load_database(cursor):
    # Open metadata file for reading
    with open("metadados.json", "r") as file:
        # Get data from file
        data = json.load(file)["table"]

        # Get all keys from the data dictionary
        keys = data.keys()
        create_table(cursor, keys)

        # Create a list of tuples from the data
        tuples = list(zip(*[data[key] for key in keys]))

        # Iterate over tuples
        for tuple in tuples:
            # Convert tuple data to string
            tuple = [str(column) for column in tuple]
            # Create a string of column values separated by comma
            values = ", ".join(tuple)
            # Create a string of column names separated by comma
            columns = ", ".join(keys)
            # Insert tuple into table
            insert_query = f"INSERT INTO data({columns}) VALUES ({values})"
            cursor.execute(insert_query)
