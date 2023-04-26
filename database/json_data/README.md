This folder is intended to store the Yelp JSON data files and the 2010 population dataset, 
which are required to run the data_import.py script. Due to their large size, these files are not included 
in the repository. To run the script, you need to download the following files:

1. Yelp JSON data files from the Yelp Dataset Challenge:
   - yelp_academic_dataset_business.json
   - yelp_academic_dataset_checkin.json
   - yelp_academic_dataset_review.json

   You can obtain the dataset by visiting the following link and accepting the terms and conditions:

   https://www.kaggle.com/datasets/yelp-dataset/yelp-dataset 

2. 2010 population dataset from Kaggle:
   - population_by_zip_2010.csv

   You can obtain the dataset by visiting the following link:

   https://www.kaggle.com/datasets/census/us-population-by-zip-code?select=population_by_zip_2010.csv

3. US Household Income Statistics from Kaggle:
   - US_Income_Kaggle.csv

   You can obtain the dataset by visiting the following link:

   https://www.kaggle.com/datasets/goldenoakresearch/us-household-income-stats-geo-locations/versions/1?select=US_Income_Kaggle.csv


After downloading the datasets, extract the Yelp JSON files and place them along with the population_by_zip_2010.csv 
file in this folder (json_data). The data_import.py script should now be able to access and process the data.

If you are using sample files for testing purposes, make sure to replace them with the actual files 
before running the script.
