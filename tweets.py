import json

def get_tweets(json_file):
   # Opening JSON file
   with open(json_file) as file:
      data = json.load(file)
      return data

TWEETS = get_tweets('/home/matteo/airflow/dags/versailles_tweets_100.json')