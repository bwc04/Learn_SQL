# No relevance to SQL. Just a reference for a table scanner incase Kaggle limit is a concern
# this reference helps with estimating how many bytes a Job for a specific table will require
# 3TB is the 30-day limit

from google.cloud import bigquery

scan_query =    """
                SELECT *
                FROM `youtube.youtube_ads_revenue`
                WHERE type = 'job';
                """

# use a queryjobconfig object to estimate query size
run_configs = bigquery.QueryJobConfig(dry_run=True)
client = bigquery.Client()
query_run_job = client.query(scan_query, job_config=run_configs)
print("This query will process {} bytes.".format(query_run_job.total_bytes_processed))

# for setting up a safety for how much data processed
safety = 1000 * 1000 # for example say we want a safe 1 mb
safe_config = bigquery.QueryJobConfig(maximum_bytes_billed=safety)
safe_query = client.query(scan_query, job_config=safe_config)