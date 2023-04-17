from sqlalchemy import create_engine, text
import db_config
import pandas as pd

# Read SQL script
with open("database/db_creation.sql", "r") as file:
    sql_script = file.read()

# Connect to the database
engine = create_engine(
    f"postgresql://{db_config.DB_SETTINGS['user']}:"
    f"{db_config.DB_SETTINGS['password']}@"
    f"{db_config.DB_SETTINGS['host']}:"
    f"{db_config.DB_SETTINGS['port']}/"
    f"{db_config.DB_SETTINGS['dbname']}"
)


def fetch_reviews():
    query = text("SELECT * FROM review LIMIT 10;")
    with engine.connect() as connection:
        result = connection.execute(query)
        for row in result:
            print(row)


def show_tables():
    query = text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
    with engine.connect() as connection:
        result = connection.execute(query)
        print("Tables in the database:")
        for row in result:
            print(row[0])


def show_views():
    query = text("SELECT schemaname, viewname FROM pg_catalog.pg_views WHERE schemaname NOT IN ('pg_catalog', "
                 "'information_schema');")
    with engine.connect() as connection:
        result = connection.execute(query)
        print("Views in the database:")
        for row in result:
            print(row[0], row[1])


def show_first_2_rows_final():
    # Read the first 2 rows of the view using pandas
    df = pd.read_sql("SELECT * FROM restaurant_businessinfo_checkin_population_review LIMIT 2", engine)

    print("First 2 rows of the final view:")
    print(", ".join(df.columns))
    print(df.to_string(index=False))


if __name__ == "__main__":
    show_tables()
    fetch_reviews()
    show_views()
    # show_first_2_rows_final()
