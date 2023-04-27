import psycopg2
import json
import csv
import db_config
import pandas as pd
from datetime import datetime


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


def insert_business_info(connection, business):
    with connection.cursor() as cursor:
        sql = """
        INSERT INTO businessInfo (id, name, address, city, zipcode, latitude, longitude)
        VALUES (%s, %s, %s, %s, %s, %s, %s);
        """
        cursor.execute(sql, (business["business_id"], business["name"], business["address"],
                             business["city"], business["postal_code"], business["latitude"], business["longitude"]))


def insert_category(connection, category_name):
    with connection.cursor() as cursor:
        # Check if the category exists
        sql = """
        SELECT id FROM category WHERE name = %s;
        """
        cursor.execute(sql, (category_name,))
        result = cursor.fetchone()

        # If the category exists, return the existing ID
        if result is not None:
            return result[0]

        # If the category does not exist, insert a new category and return the new ID
        sql = """
        INSERT INTO category (name)
        VALUES (%s)
        RETURNING id;
        """
        cursor.execute(sql, (category_name,))
        connection.commit()
        return cursor.fetchone()[0]


def insert_category_in_business(connection, business_id, category_id):
    with connection.cursor() as cursor:
        sql = """
        INSERT INTO category_in_business (business_id, category_id)
        VALUES (%s, %s);
        """
        cursor.execute(sql, (business_id, category_id))
        connection.commit()


def insert_checkin(connection, business_id, date):
    with connection.cursor() as cursor:
        sql = """
        INSERT INTO checkin (business_id, date_hour, checkin_count)
        VALUES (%s, %s, 1)
        ON CONFLICT (business_id, date_hour) 
        DO UPDATE SET checkin_count = checkin.checkin_count + 1;
        """
        cursor.execute(sql, (business_id, date))
        connection.commit()


def insert_review(connection, review_id, business_id, text, date):
    with connection.cursor() as cursor:
        sql = """
        INSERT INTO review (review_id, business_id, text, date)
        VALUES (%s, %s, %s, %s);
        """
        cursor.execute(sql, (review_id, business_id, text, date))
        connection.commit()


def insert_population(connection, zipcode, population):
    with connection.cursor() as cursor:
        sql = """
        INSERT INTO population (zipcode, population)
        VALUES (%s, %s)
        ON CONFLICT (zipcode) DO UPDATE SET
        population = population.population + excluded.population;
        """
        cursor.execute(sql, (zipcode, population))
        connection.commit()


def read_csv_and_calculate_income(file_path):
    df = pd.read_csv(file_path, dtype={'Zip_Code': str})
    df['weighted_income'] = df['Mean'] * df['Households']
    aggregated_df = df.groupby('Zip_Code').agg({'weighted_income': 'sum', 'Households': 'sum'})
    aggregated_df['income'] = aggregated_df['weighted_income'] / aggregated_df['Households']
    print(aggregated_df.head(10))
    return aggregated_df.reset_index()


def insert_income(connection, zipcode, income):
    with connection.cursor() as cursor:
        sql = """
        INSERT INTO income (zipcode, income)
        VALUES (%s, %s)
        ON CONFLICT (zipcode) DO UPDATE SET
        income = excluded.income;
        """
        cursor.execute(sql, (zipcode, income))
        connection.commit()


def process_business_data(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        connection = psycopg2.connect(
            dbname=db_config.DB_SETTINGS["dbname"],
            user=db_config.DB_SETTINGS["user"],
            password=db_config.DB_SETTINGS["password"],
            host=db_config.DB_SETTINGS["host"],
            port=db_config.DB_SETTINGS["port"]
        )

        # allow the rest of the transactions work even if some of them caused error
        connection.autocommit = True

        progress_counter = 0

        for line in file:
            business = json.loads(line)

            try:
                insert_business_info(connection, business)
                if business["categories"] is not None:
                    categories = business["categories"].split(", ")

                for category_name in categories:
                    category_id = insert_category(connection, category_name.strip())
                    insert_category_in_business(connection, business['business_id'], category_id)

                progress_counter += 1

                if progress_counter % 10000 == 0:
                    print(f"{progress_counter} businesses processed")

            except Exception as e:
                print(f"Error processing business {business['business_id']}: {e}")

        print(f"Finished inserting {progress_counter} businesses in total.")

        connection.close()


def process_checkin_data(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        connection = psycopg2.connect(
            dbname=db_config.DB_SETTINGS["dbname"],
            user=db_config.DB_SETTINGS["user"],
            password=db_config.DB_SETTINGS["password"],
            host=db_config.DB_SETTINGS["host"],
            port=db_config.DB_SETTINGS["port"],
        )

        # allow the rest of the transactions work even if some of them caused error
        connection.autocommit = True

        progress_counter = 0

        for line in file:
            checkin_entry = json.loads(line)
            business_id = checkin_entry["business_id"]
            if checkin_entry["date"] is not None:
                date_list = checkin_entry["date"].split(", ")

            try:
                for date_str in date_list:
                    date_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
                    date_hour = date_obj.replace(minute=0, second=0)
                    insert_checkin(connection, business_id, date_hour)

                progress_counter += 1

                if progress_counter % 1000 == 0:
                    print(f"{progress_counter} business checkin processed")

            except Exception as e:
                print(f"Error processing checkin business {checkin_entry['business_id']}: {e}")

        print(f"Finished inserting {progress_counter} businesses in total.")

        connection.close()


def process_review_data(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        connection = psycopg2.connect(
            dbname=db_config.DB_SETTINGS["dbname"],
            user=db_config.DB_SETTINGS["user"],
            password=db_config.DB_SETTINGS["password"],
            host=db_config.DB_SETTINGS["host"],
            port=db_config.DB_SETTINGS["port"],
        )

        # allow the rest of the transactions work even if some of them caused error
        connection.autocommit = True

        progress_counter = 0

        for line in file:
            review_entry = json.loads(line)
            review_id = review_entry["review_id"]
            business_id = review_entry["business_id"]
            text = review_entry["text"]
            date = review_entry["date"]

            try:
                insert_review(connection, review_id, business_id, text, date)

                progress_counter += 1

                if progress_counter % 100000 == 0:
                    print(f"{progress_counter} reviews processed")

            except Exception as e:
                print(f"Error processing review {review_entry['review_id']}: {e}")

        print(f"Finished inserting {progress_counter} reviews in total.")

        connection.close()


def process_population_data(file_path):
    with open(file_path, "r", encoding='utf-8-sig') as csvfile:
        connection = psycopg2.connect(
            dbname=db_config.DB_SETTINGS["dbname"],
            user=db_config.DB_SETTINGS["user"],
            password=db_config.DB_SETTINGS["password"],
            host=db_config.DB_SETTINGS["host"],
            port=db_config.DB_SETTINGS["port"],
        )

        # allow the rest of the transactions work even if some of them caused error
        connection.autocommit = True

        reader = csv.DictReader(csvfile)
        progress_counter = 0

        for row in reader:
            zipcode = row['zipcode']
            population = row['population']

            try:
                insert_population(connection, zipcode, population)

                progress_counter += 1

                if progress_counter % 100000 == 0:
                    print(f"{progress_counter} population records processed")

            except Exception as e:
                print(f"Error processing population record for zipcode {zipcode}: {e}")

        print(f"Finished inserting {progress_counter} population records in total.")

        connection.close()


def process_income_data(file_path):
    with open(file_path, "r", encoding='ISO-8859-1') as csvfile:
        connection = psycopg2.connect(
            dbname=db_config.DB_SETTINGS["dbname"],
            user=db_config.DB_SETTINGS["user"],
            password=db_config.DB_SETTINGS["password"],
            host=db_config.DB_SETTINGS["host"],
            port=db_config.DB_SETTINGS["port"],
        )

        # allow the rest of the transactions work even if some of them caused error
        connection.autocommit = True

        income_data = read_csv_and_calculate_income(csvfile)

        progress_counter = 0

        for index, row in income_data.iterrows():
            zipcode = str(row['Zip_Code'])

            try:
                income = int(row['income'])
                insert_income(connection, zipcode, income)

                progress_counter += 1

                if progress_counter % 1000 == 0:
                    print(f"{progress_counter} zipcodes processed")

            except Exception as e:
                print(f"Error processing zipcode {zipcode}: {e}")

        print(f"Finished inserting {progress_counter} zipcodes in total.")

        connection.close()


def run_views_script():
    # Create the views for combining tables
    # Read SQL script
    with open("database/restaurant_businessinfo.sql", "r") as file:
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

    connection.close()


if __name__ == "__main__":
    # run_sql_script()
    # process_business_data("database/json_data/yelp_academic_dataset_business.json")
    # process_checkin_data("database/json_data/yelp_academic_dataset_checkin.json")
    # process_review_data("database/json_data/yelp_academic_dataset_review.json")
    # process_population_data('database/json_data/population_by_zip_2010.csv')
    # process_income_data('database/json_data/US_Income_Kaggle.csv')
    run_views_script()
