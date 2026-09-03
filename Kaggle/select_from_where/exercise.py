from google.cloud import bigquery

## setup

# Create a "Client" object
client = bigquery.Client()

# Construct a reference to the "openaq" dataset
dataset_ref = client.dataset("openaq", project="bigquery-public-data")

# API request - fetch the dataset
dataset = client.get_dataset(dataset_ref)

# Construct a reference to the "global_air_quality" table
table_ref = dataset_ref.table("global_air_quality")

# API request - fetch the table
table = client.get_table(table_ref)

# Preview the first five lines of the "global_air_quality" table
client.list_rows(table, max_results=5).to_dataframe()

## Exercise 1: find the countries who report pollution units in ppm
query1 =    """
            SELECT country
            FROM `bigquery-public-data.openaq.global_air_quality`
            WHERE unit = "ppm";
            """

## Exercise 2: FInd the high air quality countries. Countries with a pollution level of 0
query2 =    """
            SELECT *
            FROM `bigquery-public-data.openaq.global_air_quality`
            WHERE value = 0;
            """
query_results = client.query(query2).to_dataframe()