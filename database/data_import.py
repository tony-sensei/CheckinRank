import psycopg2
import db_config


def run_sql_script():
    # Read SQL script
    with open("database/db_creation.sql", "r") as file:
        sql_script = file.read()

    # Connect to the database
    connection = psycopg2.connect(
        dbname=db_config.DB_SETTINGS["dbname"],
        user=db_config.DB_SETTINGS["user"],
        password=db_config.DB_SETTINGS["password"],
        host=db_config.DB_SETTINGS["host"],
        port=db_config.DB_SETTINGS["port"],
    )

    # Split the SQL script into individual statements
    statements = sql_script.strip().split(';')

    # Execute each statement
    with connection.cursor() as cursor:
        for statement in statements:
            if statement:
                cursor.execute(statement)
        connection.commit()


if __name__ == "__main__":
    run_sql_script()
