from google.cloud import bigquery
import db_dtypes
import matplotlib.pyplot as plt

client = bigquery.Client()

## bitcoin example: find how many bitcoin transactions are made per day
dataset_ref = client.dataset(dataset_id="crypto_bitcoin", project="bigquery-public-data")
dataset = client.get_dataset(dataset_ref)

table_ref = dataset_ref.table(table_id="transactions")
table = client.get_table(table_ref)

# table schema  reference
for field in table.schema:
    print(field.name, field.field_type)

# Create a CTE for each transactions and it date. Currently it in TIMESTAMP format
# We are converting it to DATE format so our main query can have a easier process grouping by the dates
# The main query then uses this CTE to group by dates and count the number of transactions each day

daily_transaction_count_query = """
                                WITH transaction_date AS
                                (
                                    SELECT 
                                        `hash` AS transaction_id, 
                                        DATE(block_timestamp) AS date
                                    FROM `bigquery-public-data.crypto_bitcoin.transactions`
                                )
                                
                                SELECT date, COUNT(transaction_id) AS num_transactions
                                FROM transaction_date
                                GROUP BY date
                                ORDER BY date;
                                """     

results = client.query(daily_transaction_count_query).to_dataframe()

## plot using matplot
plt.plot(results['date'], results['num_transactions'])
plt.show()
