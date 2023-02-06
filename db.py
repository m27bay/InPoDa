import mysql.connector

db = {
    "host": "localhost",
    "user": "root",
    "password": "VagenheimDwarves3",
    "db": "soaDB"
}

conn = mysql.connector.connect(**db)
cursor = conn.cursor(dictionary=True)

def reset():
    with open('/home/matteo/airflow/dags/reset.sql', 'r') as sql_file:
        result_iterator = cursor.execute(sql_file.read(), multi=True)
        for res in result_iterator:
            print("Running query: ", res)  # representation of the query
            print(f"Affected {res.rowcount} rows" )

        conn.commit()  # commit changes

def insert_tweet(tweet_id, author_id, text, sentiment, tags, topics):
    sql = "INSERT INTO Tweets (id, author_id, text, sentiment) VALUES (%s, %s, %s, %s)"
    val = (tweet_id, author_id, text, sentiment)
    cursor.execute(sql, val)

    for tag in tags :
        sql = "INSERT INTO Hashtags (tweet_id, tag) VALUES (%s, %s)"
        val = (tweet_id, tag)
        cursor.execute(sql, val)

    for topic in topics :
        sql = "INSERT INTO Topics (tweet_id, topic) VALUES (%s, %s)"
        val = (tweet_id, topic)
        cursor.execute(sql, val)

    conn.commit()

def select(sql, val=None):
    if val == None:
        cursor.execute(sql)
    else:
        cursor.execute(sql, val)
    res = str(cursor.fetchall())
    return res