
import os
from matplotlib import pyplot as plt
import seaborn as sns

import pandas as pd
from gen_entities import gen_entities


if __name__ == "__main__":
    # Get generated entities
    entities = gen_entities()

    # Entity by their score
    entity_scores = {}
    for id, row in entities.iterrows():
        created = row["created"]
        text = row["text"]
        score = row["score"]

        if (text in entity_scores):
            entity_scores[text] += score
        else:
            entity_scores[text] = score

    # Get top 10 entities by sortedness
    size = 10
    entity_scores_sorted = sorted(entity_scores.items(), key=lambda a: a[1], reverse=True)
    entity_scores_sorted_head = [entity_scores_sorted[i][0] for i in range(size)]
    print(entity_scores_sorted_head)
    
    # Filter entities by only the top 10
    entities = entities[(entities.text.isin(entity_scores_sorted_head))]

    # Display histplot of the top 10 entities over time
    plt.figure(figsize=(12, 6))
    sns.histplot(entities, x="created", hue="text", weights="score", element="poly", bins=60)
    plt.xlabel('Time')
    plt.ylabel('Score')
    plt.title('Wallstreetbets entities over time')
    plt.show()