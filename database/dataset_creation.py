import pandas as pd
from sqlalchemy import create_engine
import db_config


def extract_info(col_name, value):
    try:
        day_map = {'mon': 1, 'tue': 2, 'wed': 3, 'thur': 4, 'fri': 5, 'sat': 6, 'sun': 7}
        day, time_range = col_name.split("_", 1)  # Split the column name based on the first underscore only
        start, end = map(int, time_range.split("_"))
        mid_time = (start + end) / 2
        return day_map[day], mid_time, value
    except ValueError:
        print(f"Error processing column name: {col_name}")
        raise


def split_reviews(aggregated_text):
    return aggregated_text.split("|||")


def main():
    # Connect to the database using the provided configuration in db_config
    engine = create_engine(f"postgresql://{db_config.DB_SETTINGS['user']}"
                           f":{db_config.DB_SETTINGS['password']}"
                           f"@{db_config.DB_SETTINGS['host']}"
                           f":{db_config.DB_SETTINGS['port']}"
                           f"/{db_config.DB_SETTINGS['dbname']}")

    # Read the data from the view
    query = "SELECT * FROM main_add_reviewcount_restaurantcount_income"
    df = pd.read_sql(query, engine)

    # Normalize check-in numbers
    time_slots = [
        "mon_0_6", "mon_7_10", "mon_11_13", "mon_14_17", "mon_18_20", "mon_21_23",
        "tue_0_6", "tue_7_10", "tue_11_13", "tue_14_17", "tue_18_20", "tue_21_23",
        "wed_0_6", "wed_7_10", "wed_11_13", "wed_14_17", "wed_18_20", "wed_21_23",
        "thur_0_6", "thur_7_10", "thur_11_13", "thur_14_17", "thur_18_20", "thur_21_23",
        "fri_0_6", "fri_7_10", "fri_11_13", "fri_14_17", "fri_18_20", "fri_21_23",
        "sat_0_6", "sat_7_10", "sat_11_13", "sat_14_17", "sat_18_20", "sat_21_23",
        "sun_0_6", "sun_7_10", "sun_11_13", "sun_14_17", "sun_18_20", "sun_21_23"
    ]
    for slot in time_slots:
        df[slot] = (df[slot] / df['range_in_days'] * 365).round(2)

    # Drop unnecessary columns
    df_main = df.drop(columns=['id', 'name', 'business_id', 'address', 'city', 'zipcode', 'range_in_days'])

    # Save the dataframe to a CSV file
    df_main.to_csv("machine_learning/data/main.csv", index=False)

    print("CSV file created: main.csv")

    # Create a new DataFrame to store the desired data
    new_df = pd.DataFrame(columns=["longitude", "latitude", "zipcode", "population", "day", "time", "checkinNum",
                                   "review_count", "restaurant_count", "income"])

    # Create a new list to store the desired data
    new_data = []

    # Calculate the total number of iterations
    total_iterations = len(df) * len(time_slots)

    # Iterate through the original DataFrame
    for index, row in df.iterrows():
        for idx, col_name in enumerate(time_slots):
            day, time, checkin_num = extract_info(col_name, row[col_name])
            new_row = {
                "longitude": row["longitude"],
                "latitude": row["latitude"],
                "zipcode": row["zipcode"],
                "population": row["population"],
                "day": day,
                "time": time,
                "checkinNum": checkin_num,
                "review_count": row["review_count"],
                "restaurant_count": row["restaurant_count"],
                "income": row["income"]
            }
            new_data.append(new_row)

            # Calculate and print the progress
            current_iteration = index * len(time_slots) + idx + 1
            progress_percentage = (current_iteration / total_iterations) * 100
            if current_iteration % 1000 == 0:
                print(f"Processed {current_iteration}/{total_iterations} ({progress_percentage:.2f}%)")

    # Convert the list of dictionaries to a DataFrame
    new_df = pd.DataFrame(new_data)

    # Save the new DataFrame to a CSV file
    new_df.to_csv("machine_learning/data/statistical.csv", index=False)

    print("CSV file created: statistical.csv")

    # Create a list to store the extracted reviews
    reviews_list = []

    # Calculate the total number of rows in the DataFrame
    total_rows = len(df)

    # Iterate through the DataFrame
    for index, row in df.iterrows():
        # Split the aggregated_text using "|||" as the separator
        reviews = row["aggregated_text"].split("|||")

        # Add each review to the list
        for review in reviews:
            reviews_list.append({"review": review})

        # Calculate and print the progress
        progress_percentage = ((index + 1) / total_rows) * 100
        if (index + 1) % 1000 == 0:
            print(f"Processed {index + 1}/{total_rows} ({progress_percentage:.2f}%)")

    # Convert the list of dictionaries to a DataFrame
    reviews_df = pd.DataFrame(reviews_list)

    # Save the DataFrame to a CSV file
    reviews_df.to_csv("machine_learning/data/reviews.csv", index=False)

    print("CSV file created: reviews.csv")


if __name__ == "__main__":
    main()



