from google.cloud import bigquery
import pandas as pd

client = bigquery.Client()
dataset_ref = client.dataset("youtube", project="hackernews-505120")
dataset = client.get_dataset(dataset_ref)

tables = list(client.list_tables(dataset))
for table in tables:
    print(table.table_id)

table_ref = dataset_ref.table("youtube_ads_revenue")
table = client.get_table(table_ref)

data = pd.DataFrame(client.list_rows(table, max_results=5))
print(data)

# table is confirmed, now to run a query on it
ex_query =  """
            SELECT Date
            FROM `youtube.youtube_ads_revenue`
            WHERE Date > '2024-01-01'
            LIMIT 10;
            """

# submit the query
query_job = client.query(ex_query)
query_results = pd.DataFrame(query_job)
print(query_results)