DROP TABLE IF EXISTS Hashtags;
DROP TABLE IF EXISTS Topics;
DROP TABLE IF EXISTS Tweets;

CREATE TABLE Tweets (
    id VARCHAR(30),
    author_id VARCHAR(30) NOT NULL,
    text VARCHAR(1000) NOT NULL,
    sentiment VARCHAR(30) NOT NULL,
    CONSTRAINT pk_tweets PRIMARY KEY (id)
);

CREATE TABLE Hashtags (
    tweet_id VARCHAR(30),
    tag VARCHAR(50) NOT NULL,
    CONSTRAINT pk_hashtags PRIMARY KEY (tweet_id, tag),
    CONSTRAINT fk_hashtags FOREIGN KEY (tweet_id) REFERENCES Tweets(id)
);

CREATE TABLE Topics (
    tweet_id VARCHAR(30),
    topic VARCHAR(50) NOT NULL,
    CONSTRAINT pk_topics PRIMARY KEY (tweet_id, topic),
    CONSTRAINT fk_topics FOREIGN KEY (tweet_id) REFERENCES Tweets(id)
);