import os

import matplotlib.pyplot as plt
import pandas as pd

from gen_entities import gen_entities

if __name__ == "__main__":
    # Get generated entities
    entities = gen_entities()

    # Dict of entity scores
    entity_scores = {}
    for id, row in entities.iterrows():
        created = row["created"]
        text = row["text"]
        score = row["score"]

        if (text in entity_scores):
            entity_scores[text] += score
        else:
            entity_scores[text] = score

    # Sort the entity scores and print top 10
    entity_scores_sorted = sorted(entity_scores.items(), key=lambda a: a[1], reverse=True)
    size = 10
    for i in range(size):
        print(entity_scores_sorted[i])

    fig, ax = plt.subplots()

    names = [s[0] for s in entity_scores_sorted[:10]]
    counts = [s[1] for s in entity_scores_sorted[:10]]

    # Plot the top 10 most common entities
    ax.bar(names, counts)
    ax.set_ylabel('score')
    ax.set_title('Reddit post entities by score')

    plt.show()