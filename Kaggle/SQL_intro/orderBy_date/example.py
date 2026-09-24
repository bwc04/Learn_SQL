from google.cloud import bigquery
import pandas as pd

# 2015 accidents table. Table includes every accident
client = bigquery.Client()
dataset_ref = client.dataset(dataset_id="nhtsa_traffic_fatalities", project="bigquery-public-data")
dataset = client.get_dataset(dataset_ref)

table_ref = dataset_ref.table("accident_2015")
table = client.get_table(table_ref)

# table reference
print(pd.DataFrame(client.list_rows(table, max_results=5)))

# query to find the number of accidents that happened every day of the week where at least one fatality occured
# this can help us find the day of the week where most accidents occur. I would likley assume it to be either friday or the weekend
highest_acc_day_query = """
                        SELECT 
                            EXTRACT(DAYOFWEEK from timestamp_of_crash) AS day_of_week, 
                            COUNT(consecutive_number) AS accidents_count
                        FROM `bigquery-public-data.nhtsa_traffic_fatalities.accident_2015`
                        WHERE number_of_fatalities > 0
                        GROUP BY day_of_week
                        ORDER BY day_of_week;
                        """

result = pd.DataFrame(client.query(highest_acc_day_query))
print(result)
