from textblob import TextBlob
from textblob_fr import PatternTagger, PatternAnalyzer

def sentiment_classification(text):
    blob = TextBlob(text, pos_tagger=PatternTagger(), analyzer=PatternAnalyzer())
    analysis = blob.sentiment
    if analysis[0] > 0:
        sentiment = 'positif'
    elif analysis[0] < 0:
        sentiment = 'negatif'
    else:
        sentiment = 'neutre'
    if analysis[1] >= 0.65:
        sentiment += ", très subjectif"
    elif analysis[1] >= 0.3:
        sentiment += ", subjectif"
    else:
        sentiment += ", objectif"
    return sentiment