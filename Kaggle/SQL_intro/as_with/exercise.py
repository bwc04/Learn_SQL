from google.cloud import bigquery
import db_dtypes
import matplotlib.pyplot as plt

## setup
# Dataset about taxi trips in the city of Chicago. The queries will help answer how much slower traffic moves
# when traffic volume is high. 

# Create a "Client" object
client = bigquery.Client()

# Construct a reference to the "chicago_taxi_trips" dataset
dataset_ref = client.dataset("chicago_taxi_trips", project="bigquery-public-data")

# API request - fetch the dataset
dataset = client.get_dataset(dataset_ref)

# find the correct table name
tables = client.list_tables(dataset)
for table in tables:
    print(table.table_id)

# table name is taxi_trips
table_ref = dataset_ref.table("taxi_trips")
table = client.get_table(table_ref)

# data reference. examine schema and check for any issues regarding data quality
for field in table.schema:
    print("{} : {}".format(field.name, field.field_type))

print(client.list_rows(table, max_results=5).to_dataframe())

# This data could be too old and the traffic trends might not apply nowadays.
# This query will count the number of trips each year

num_trips_query =   """
                    SELECT 
                        EXTRACT(YEAR FROM trip_start_timestamp) AS year,
                        COUNT(*) AS num_trips
                    FROM `bigquery-public-data.chicago_taxi_trips.taxi_trips`
                    GROUP BY year
                    ORDER BY year;
                    """
# set a safe as this table is massive
max_bytes = 10 ** 10
safe_config = bigquery.QueryJobConfig(maximum_bytes_billed=max_bytes)
num_trips_query_job = client.query(num_trips_query, job_config=safe_config)
num_trips = num_trips_query_job.to_dataframe()
print(num_trips)

# taking a look at rides from 2016. Find the number of trips each month in the year 2016
num_trips_monthly2016_query =   """
                                SELECT 
                                    EXTRACT(MONTH FROM trip_start_timestamp) AS month,
                                    COUNT(*) AS num_trips
                                FROM `bigquery-public-data.chicago_taxi_trips.taxi_trips`
                                WHERE EXTRACT(YEAR FROM trip_start_timestamp) = 2016
                                GROUP BY month
                                ORDER BY month;
                                """

num_trips_monthly2016_job = client.query(num_trips_monthly2016_query, job_config=safe_config)
num_trips_monthly2016 = num_trips_monthly2016_job.to_dataframe()
print(num_trips_monthly2016)

# Query that finds the number of trips and average speed of the rides for each hour of the day throughout
# the entire range of dates in the dataset
# CTE of each rides, hour they occured
trips_speed_daily_query =   """
                            WITH trip_hour AS
                            (
                                SELECT 
                                    EXTRACT(HOUR FROM trip_start_timestamp) AS hour_of_day,
                                    trip_miles, 
                                    trip_seconds
                                FROM `bigquery-public-data.chicago_taxi_trips.taxi_trips`
                                WHERE 
                                    trip_start_timestamp > "2016-01-01" 
                                    AND trip_start_timestamp < "2016-04-01"
                                    AND trip_seconds > 0 AND trip_miles > 0
                            )

                            SELECT
                                hour_of_day,
                                (3600 * SUM(trip_miles) / SUM(trip_seconds)) AS avg_mph,
                                COUNT(*) AS num_trips
                            FROM trip_hour
                            GROUP BY hour_of_day
                            ORDER BY hour_of_day;
                            """

trips_speed_daily_job = client.query(trips_speed_daily_query, job_config=safe_config)
trips_speed_daily = trips_speed_daily_job.to_dataframe()
print(trips_speed_daily)
