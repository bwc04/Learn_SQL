from google.cloud import bigquery
import db_dtypes
import matplotlib.pyplot as plt

## This example uses a dataset regarding a record of Github projects and it corresponding licenses and files
client = bigquery.Client()

# github dataset
dataset_ref = client.dataset("github_repos", project="bigquery-public-data")
dataset = client.get_dataset(dataset_ref)

# license table
license_table_ref = dataset_ref.table("licenses")
license_table = client.get_table(license_table_ref)

# sample files
file_table_ref = dataset_ref.table("sample_files")
file_table = client.get_table(file_table_ref)

# quick table reference
# print(client.list_rows(license_table, max_results=5).to_dataframe())
# print(client.list_rows(file_table, max_results=5).to_dataframe())

'''
query that determines how many repos are under each each license
Note we would have to utilize distinct to count the unique number of repos each license
since each repo can appear multiple times due to multiple files
'''

repos_per_license_query =   """
                            SELECT
                                l.license,
                                COUNT(DISTINCT gr.repo_name) AS repo_count
                            FROM 
                            `bigquery-public-data.github_repos.licenses` AS l LEFT JOIN
                            `bigquery-public-data.github_repos.sample_files` AS gr
                            ON l.repo_name = gr.repo_name
                            GROUP BY l.license
                            ORDER BY repo_count ASC;
                            """
'''
We also used LEFT JOIN because we still want to include every license even if their is no repo under
that license. If we used a INNER JOIN, any licenses without matches would not even appear. With a LEFT JOIN,
we can gurantee all licenses will be included.
'''

# run the query under safe conditions
# returns the number of unqiue repos per license
safe_config = bigquery.QueryJobConfig(maximum_bytes_billed=10**10)
query_job = client.query(repos_per_license_query, job_config=safe_config)
repos_per_license = query_job.to_dataframe()
print(repos_per_license)
