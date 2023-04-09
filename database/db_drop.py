import psycopg2
import db_config


def drop_tables(connection):
    with connection.cursor() as cursor:
        sql = """
        DROP TABLE IF EXISTS category_in_business;
        DROP TABLE IF EXISTS review;
        DROP TABLE IF EXISTS checkin;
        DROP TABLE IF EXISTS category;
        DROP TABLE IF EXISTS businessInfo;
        DROP TABLE IF EXISTS population;
        """

        cursor.execute(sql)
        connection.commit()


def main():
    connection = psycopg2.connect(
        dbname=db_config.DB_SETTINGS["dbname"],
        user=db_config.DB_SETTINGS["user"],
        password=db_config.DB_SETTINGS["password"],
        host=db_config.DB_SETTINGS["host"],
        port=db_config.DB_SETTINGS["port"],
    )

    drop_tables(connection)
    connection.close()
    print("All tables have been dropped.")


if __name__ == "__main__":
    main()
