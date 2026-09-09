## setup
# education data from the world bank. 
from google.cloud import bigquery

# Create a "Client" object
client = bigquery.Client()

# Construct a reference to the "world_bank_intl_education" dataset
dataset_ref = client.dataset("world_bank_intl_education", project="bigquery-public-data")

# API request - fetch the dataset
dataset = client.get_dataset(dataset_ref)

# Construct a reference to the "international_education" table
table_ref = dataset_ref.table("international_education")

# API request - fetch the table
table = client.get_table(table_ref)

# Preview the first five lines of the "international_education" table
client.list_rows(table, max_results=5).to_dataframe()

## exercises

# Write a query to find the countries that spends the largest fraction of their GDP on their education system.
# utilize the data with the indicator code SE.XPD.TOTL.GD.ZS from years 2010-2017
# include the country name
# use AVG() and avg_ed_spending_pct for the average expenditure
# order results by the countries that spend the most to least

largest_expenditure_query = """
                            SELECT country_name, AVG(value) AS avg_ed_spending_pct
                            FROM `bigquery-public-data.world_bank_intl_education.international_education`
                            WHERE year >= 2010 AND year <= 2017 AND indicator_code = "SE.XPD.TOTL.GD.ZS"
                            GROUP BY country_name
                            ORDER BY avg_ed_spending_pct DESC;
                            """
# Set up the query (cancel the query if it would use too much of 
# your quota, with the limit set to 1 GB)
safe_config = bigquery.QueryJobConfig(maximum_bytes_billed=10**10)
country_spend_pct_query_job = client.query(country_spend_pct_query, job_config=safe_config)

# API request - run the query, and return a pandas DataFrame
country_spending_results = country_spend_pct_query_job.to_dataframe()

# View top few rows of results
print(country_spending_results.head())

# a query that finds all indicator names and codes with at least 175 rows in 2016
# Order from most frequent indicator codes to least frequent
indicator_freq_query = """
                       SELECT indicator_name, indicator_code, COUNT(*) AS num_rows
                       FROM `bigquery-public-data.world_bank_intl_education.international_education`
                       WHERE year = 2016
                       GROUP BY indicator_name, indicator_code
                       HAVING num_rows >= 175
                       ORDER BY num_rows DESC;
                       """
# Set up the query
safe_config = bigquery.QueryJobConfig(maximum_bytes_billed=10**10)
code_count_query_job = client.query(code_count_query, job_config=safe_config)

# API request - run the query, and return a pandas DataFrame
code_count_results = code_count_query_job.to_dataframe()

# View top few rows of results
print(code_count_results.head())