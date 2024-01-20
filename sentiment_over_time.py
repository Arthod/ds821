
import os
from matplotlib import pyplot as plt
import matplotlib as mpl
import seaborn as sns

import pandas as pd
from gen_sentiment_afinn import gen_sentiment_afinn
from gen_entities import gen_entities


if __name__ == "__main__":
    entity_name = "GME"

    sentiments = gen_sentiment_afinn()
    entities = gen_entities()

    # Find set of post_ids that have that entity
    post_ids = set()
    for (id, row) in entities.iterrows():
        post_id = row["post_id"]
        text = row["text"]
        
        if (text == entity_name):
            post_ids.add(post_id)

    # Filter sentiments by post id
    sentiments = sentiments.filter(items=post_ids, axis=0)

    # Plot
    plt.figure(figsize=(12, 6))
    sns.histplot(sentiments, x="created", weights="sentiment", element="poly", bins=60)
    plt.xlabel('Time')
    plt.ylabel('Sentiment')
    plt.title(f'{entity_name} sentiment over time')
    plt.show()