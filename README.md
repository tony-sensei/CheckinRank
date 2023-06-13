# CheckinRank

This project will utilize the Yelp dataset to predict the restaurants' wait time, food quality, environmental quality, 
service quality based on customer reviews using DistilBERT, and find their correlation with the restaurants' check-in number.

## Demonstration

To understand how our project works, we recommend running `demo.ipynb` and `Statistical model.Rmd`. 

- `demo.ipynb`: This Jupyter notebook contains a simple demonstration of our machine learning model. It provides a 
step-by-step guide to  how we preprocess our data, train our model, and evaluate its performance.

- `Statistical model.Rmd`: This R Markdown document demonstrates our statistical modeling process. It shows how we fit 
our data to the model, interpret the results, and draw conclusions.

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

## Dataset Creation

To generate the necessary datasets for the project, run the `dataset_creation.py` script:

```bash
python3 database/dataset_creation.py
```

This script will create three CSV files in the `machine_learning/data` directory:

1. `main.csv`: This dataset will be used for predicting check-ins. It contains features like longitude, latitude, population, day, time, and the check-in number.
2. `statistical.csv`: This dataset will be used for statistical analysis. It includes longitude, latitude, zipcode, population, day, time, and check-in number.
3. `reviews.csv`: This dataset contains all the reviews and will be used for training the NLP model.


## Feature extraction using DistilBERT

To extracting the features from customer reviews, check and run the `machine_learning/reviews_training.ipynb`:

