from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator

from tweets import TWEETS
from sentiment import sentiment_classification
from db import reset, insert_tweet

# Define the default arguments for the DAG
default_args = {
    'owner':'airflow',
    'depends_on_past': False,
    'start_date': datetime(2022, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=2),
}

def author_identification(ti, tweets):
    authors = [tweet["author_id"] for tweet in tweets]

    ti.xcom_push(key='authors', value=authors)
    print(f"authors_id : {authors}")

def hashtags_extraction(ti, tweets):
    tags = [
        [hashtag["tag"] for hashtag in tweet["entities"]["hashtags"]]
        if "entities" in tweet and "hashtags" in tweet["entities"] else []
        for tweet in tweets
    ]

    ti.xcom_push(key='tags', value=tags)
    print(f"tags : {tags}")

def sentiment_analysis(ti, tweets):
    sentiments = [sentiment_classification(tweet["text"]) for tweet in tweets]

    ti.xcom_push(key='sentiments', value=sentiments)
    print(f"sentiments : {sentiments}")

def topic_identification(ti, tweets):
    topics = [
        [topic["name"] for topic in tweet["topics"]]
        if "topics" in tweet else []
        for tweet in tweets
    ]

    ti.xcom_push(key='topics', value=topics)
    print(f"topics : {topics}")

def tweet_processing(ti, tweets):
    reset()
    nb_tweets = len(TWEETS)

    authors = ti.xcom_pull(task_ids='author_identification', key='authors')
    tags = ti.xcom_pull(task_ids='hashtags_extraction', key='tags')
    sentiments = ti.xcom_pull(task_ids='sentiment_analysis', key='sentiments')
    topics = ti.xcom_pull(task_ids='topic_identification', key='topics')

    for i in range(nb_tweets):
        id = tweets[i]['id']
        text = tweets[i]['text']
        insert_tweet(id, authors[i], text, sentiments[i], tags[i], topics[i])

        print(f"{id, authors[i], text, sentiments[i], tags[i], topics[i]}")

# A DAG represents a workflow, a collection of tasks
with DAG(
    dag_id="InPoDa_dag",
    default_args=default_args,
    start_date=datetime(2022, 1, 1),
    schedule_interval='@daily'
) as dag:
    
    auth_id = PythonOperator(
        task_id="author_identification",
        python_callable=author_identification,
        op_kwargs={"tweets": TWEETS},
        dag=dag
    )

    tags = PythonOperator(
        task_id="hashtags_extraction",
        python_callable=hashtags_extraction,
        op_kwargs={"tweets": TWEETS},
        dag=dag
    )

    sentiment = PythonOperator(
        task_id="sentiment_analysis", 
        python_callable=sentiment_analysis,
        op_kwargs={"tweets": TWEETS},
        dag=dag
    )

    topics = PythonOperator(
        task_id="topic_identification", 
        python_callable=topic_identification,
        op_kwargs={"tweets": TWEETS},
        dag=dag
    )

    main = PythonOperator(
        task_id="tweet_processing", 
        python_callable=tweet_processing,
        op_kwargs={"tweets": TWEETS},
        dag=dag
    )

    [auth_id, tags, sentiment, topics] >> main