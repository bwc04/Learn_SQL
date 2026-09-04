from google.cloud import bigquery
import pandas as pd

client = bigquery.Client()
dataset_ref = client.dataset(dataset_id="youtube", project="hackernews-505120")
dataset = client.get_dataset(dataset_ref)

table_ref = dataset_ref.table("youtube_ads_revenue")
table = client.get_table(table_ref)

# table overview
table_overview = client.list_rows(table, max_results=5)
print(pd.DataFrame(table_overview))

# query using GROUP BY, HAVING, COUNT
# this query will find the group of ad revenue numbers that are seen across more then one day
query = """
        SELECT `Ads Revenue _Mn_`, COUNT(`Date`) AS frequency
        FROM `youtube.youtube_ads_revenue`
        GROUP BY `Ads Revenue _Mn_`
        HAVING COUNT(`Date`) > 1;
        """

# this should theoritically return a empty dataframe because it very rare for days to have the exact same
# ad revenue count considering we are dealing with numbers in the thousands. Even numbers off by 1.
results = pd.DataFrame(client.query(query))
print(results)
