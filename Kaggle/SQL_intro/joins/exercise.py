from google.cloud import bigquery
import db_dtypes

client = bigquery.Client()

## SQL service that categorizes users into categories based of their technological expertise
# For a user to demonstrate technological expertise, they must helped answer questions related to the topic.
# This service can allow people to hire these experts for in-depth help

dataset_ref = client.dataset("stackoverflow", project="bigquery-public-data")
dataset = client.get_dataset(dataset_ref)

## explore the tables available in the stackoverflow dataset
tables = client.list_tables(dataset)
tables_list = [table.table_id for table in tables]
# print(tables_list)

## Review the relevant tables
# Construct a reference to the posts_answers and post_questions table
answers_table_ref = dataset_ref.table("posts_answers")
questions_table_ref = dataset_ref.table("posts_questions")

# preview both tables
# answer_table = client.get_table(answers_table_ref)
# questions_table = client.get_table(questions_table_ref)
# print(client.list_rows(answers_table_ref, max_results=5).to_dataframe())
# print(client.list_rows(questions_table, max_results=5).to_dataframe())

## Query that utilizes WHERE LIKE to select the id, title and owner user id from the post_questions table
# restrict results to rows that contain "biqguery" in tags column
# include rows where there is other text in addtion to bigquery.

bigquery_query =    """
                    SELECT id, title, owner_user_id
                    FROM `bigquery-public-data.stackoverflow.posts_questions`
                    WHERE tags LIKE '%bigquery%';
                    """

# run query
safe_config = bigquery.QueryJobConfig(maximum_bytes_billed=10**10)
bigquery_query_job = client.query(bigquery_query, job_config=safe_config)
bigquery_results = bigquery_query_job.to_dataframe()
print(bigquery_results)


## Query that returns the id, body, owner_user_id from post_answers table for answers related to bigquery
# Utilize post_questions to determine each posts centered topic. Then you can determine the tag for each answer

bigquery_answers_query =    """
                            SELECT pq.id, pa.body, pa.owner_user_id
                            FROM 
                                `bigquery-public-data.stackoverflow.posts_answers` AS pa
                                INNER JOIN
                                `bigquery-public-data.stackoverflow.posts_questions` AS pq
                                ON pa.parent_id = pq.id
                            WHERE pq.tags LIKE '%bigquery%';
                            """
safe_config2 = bigquery.QueryJobConfig(maximum_bytes_billed=27*10**10)
bigquery_answers_query_job = client.query(bigquery_answers_query, job_config=safe_config2)
bigquery_answers = bigquery_answers_query_job.to_dataframe()
print(bigquery_answers)

## Query, update upon the previous query. This time we want a list of users who answered many questions
# We want users that have answered at least one question with the bigquery tag
# 2 columns: user_id which is the owner_user_id from post_answers and number_of_answers

bigquery_experts_query =    """
                            SELECT
                                pa.owner_user_id AS user_id,
                                COUNT(*) AS number_of_answers
                            FROM
                                `bigquery-public-data.stackoverflow.posts_answers` AS pa
                                INNER JOIN
                                `bigquery-public-data.stackoverflow.posts_questions` AS pq
                                ON pa.parent_id = pq.id
                            WHERE pq.tags LIKE '%bigquery%'
                            GROUP BY user_id
                            HAVING number_of_answers >= 1
                            ORDER BY number_of_answers DESC;
                            """

biqquery_experts_query_job = client.query(bigquery_experts_query, job_config=safe_config)
bigquery_experts = biqquery_experts_query_job.to_dataframe()
print(bigquery_experts)

## Additional Exercise: imagaine a website backend that allows you to contact any expert based of any topic.
# My solution to this would be to a function that simulate a query each time a user enters a topic
# The query runs whenever a user enters a topic and finds the top users with the most answered questions related to that topic

# this would be the query defaulted
experts_query =     """
                    SELECT
                        pa.owner_user_id AS user_id,
                        pa.owner_display_name AS username,
                        COUNT(*) AS related_questions_answered
                    FROM
                        `bigquery-public-data.stackoverflow.posts_answers` AS pa
                        INNER JOIN
                        `bigquery-public-data.stackoverflow.posts_questions` AS pq
                        ON pa.parent_id = pq.id
                    WHERE pq.tags LIKE '%[USER_INPUTTED_TOPIC]%'
                    GROUP BY user_id, username
                    HAVING related_questions_answered > 1
                    ORDER BY related_questions_answered DESC
                    LIMIT 5;
                    """
'''
Whenever a user enters a topic, the query runs with the topic replaceing [USER_INPUTTED_TOPIC].
The user will get recieve a list of the top 5 users who have answered the most questions regarding that topic.
It also includes the users username so they can be contacted, along with the count of the questions answered.
'''
