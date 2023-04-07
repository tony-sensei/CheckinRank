from sqlalchemy import create_engine, text
import db_config

# Read SQL script
with open("db_creation.sql", "r") as file:
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
    query = text("SELECT * FROM reviews LIMIT 10;")
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


if __name__ == "__main__":
    show_tables()
    # fetch_reviews()
