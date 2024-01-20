
from afinn import Afinn
import pandas as pd
import os

import string

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

stopwords = set(stopwords.words("english"))

# Get afinn model
afinn = Afinn()

def get_sentiment(text):
    text = word_tokenize(text)
    
    # Preprocess
    text = [word.lower() for word in text] # Make all characters lower
    text = [word for word in text if word not in stopwords] # Remove stopwords
    text = [word for word in text if word not in string.punctuation] # Remove punctuation

    # Find the sentiment and normalize
    sentiment = sum(afinn.score(word) for word in text)
    if (len(text) == 0):
        return 0
    sentiment = sentiment / len(text)
    
    return sentiment

def gen_sentiment_afinn():
    # If file exists, read it.
    if (os.path.exists("preprocessed/sentiments.csv")):
        rwsb = pd.read_csv("preprocessed/sentiments.csv")
        rwsb['created'] = pd.to_datetime(rwsb['created'])
    
    else:        
        # Read data file as csv
        rwsb = pd.read_csv("data/reddit_wsb.csv")
        num_posts = len(rwsb)

        # Preprocess some of the column
        rwsb['created'] = pd.to_datetime(rwsb['created'], unit="s")


        sentiments = []    
        for post_id, (title, body) in enumerate(zip(rwsb["title"], rwsb["body"])):
            # Get text
            if (str(body) == "nan"):
                # If there is no body, the text is only the title.
                text = title
            else:
                # Otherwise we concatenate the title and body.
                text = f"{title} {body}"

            # Calculate sentiment
            sentiment = get_sentiment(text)
            sentiments.append(sentiment)

            # Verbosity
            if (post_id % 500 == 0):
                print(f"{post_id} / {num_posts}")


        # Add sentiments as column to dataframe and save as preprocessed .csv
        rwsb = rwsb.assign(sentiment=sentiments)
        rwsb.to_csv("preprocessed/sentiments.csv")

    return rwsb

if __name__ == "__main__":
    gen_sentiment_afinn()