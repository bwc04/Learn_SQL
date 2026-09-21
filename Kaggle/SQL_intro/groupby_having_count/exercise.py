## setup
from google.cloud import bigquery

# Create a "Client" object
client = bigquery.Client()

# Construct a reference to the "hacker_news" dataset
dataset_ref = client.dataset("hacker_news", project="bigquery-public-data")

# API request - fetch the dataset
dataset = client.get_dataset(dataset_ref)

# Construct a reference to the "full" table
table_ref = dataset_ref.table("full")

# API request - fetch the table
table = client.get_table(table_ref)

# Preview the first five lines of the table
client.list_rows(table, max_results=5).to_dataframe()

## excersises

# query that returns all authors with more then 10,000 posts on hackernews. Include the post counts
# name that column NumPosts
prolific_commenters_query = """
                            SELECT `by` AS author, COUNT(*) AS NumPosts
                            FROM `bigquery-public-data.hacker_news.full`
                            GROUP BY `by`
                            HAVING COUNT(*) > 10000;
                            """ # Your code goes here

# Set up the query (cancel the query if it would use too much of 
# your quota, with the limit set to 1 GB)
safe_config = bigquery.QueryJobConfig(maximum_bytes_billed=10**10)
query_job = client.query(prolific_commenters_query, job_config=safe_config)

# API request - run the query, and return a pandas DataFrame
prolific_commenters = query_job.to_dataframe()

# View top few rows of results
print(prolific_commenters.head())

# query that finds the number of deleted columns
deleted_comments_query = """
                         SELECT COUNT(*) AS deleted_comments
                         FROM `bigquery-public-data.hacker_news.full`
                         WHERE deleted = True;
                         """
results = client.query(deleted_comments_query)
print(results.to_dataframe())