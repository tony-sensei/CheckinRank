# CheckinRank

This project will utilize the Yelp dataset to predict the rank of passenger flows in any specific area of California 
by zip code using machine learning methods.

## Prerequisites

Before you begin, make sure you have the following installed:

- Python 3.x
- PostgreSQL

## Configuration

1. Rename the `db_config_sample.py` file to `db_config.py`.

```bash
mv db_config_sample.py db_config.py
```

2. Open the db_config.py file and update the following information with your PostgreSQL database credentials:

```
DB_NAME: The name of your database.
DB_USER: The username for your database.
DB_PASSWORD: The password for your database.
DB_HOST: The hostname for your database (use 'localhost' if running on the same machine).
DB_PORT: The port number for your PostgreSQL database (default is 5432).
```

## Installation

To install the required dependencies for the project, navigate to the project directory and run the following command:

```bash
pip install -r requirements.txt
```

This command will install the Python packages listed in the requirements.txt file.

## Database Setup

1. Follow the instructions in `database/json_data/README.md` to download and 
set up the required JSON and csv data files.

2. a. Create tables and insert row data to the created tables in the database

To create tables and insert row data to the created tables in the database, run the `data_import.py` script:

```bash
python database/data_import.py
```

This script will read the SQL statements from the `db_creation.sql` file, the json and csv files 
from database/json_data folder
and create the tables with raw data in your PostgreSQL database.
*Note: the process will be long*

2. b. Drop tables in the databases

Drops all tables in the database. **Warning: Running this script will delete all data from the database. 
Use it with caution.**

```bash
python database/db_drop.py
```

Please note that running db_drop.py will delete all data from your database, so use it with caution 
and only when necessary.


3. Test the database

To test if the tables were created correctly in the database, run the `test_db.py` script:

```bash
python database/test_db.py
```

This script will display the list of tables in the database and fetch the first 10 rows from the `reviews` table.

