
import pandas as pd
import spacy
import os

def gen_entities():

    # If file exists, read it.
    if (os.path.exists("preprocessed/entities.csv")):
        entities = pd.read_csv("preprocessed/entities.csv")
        entities['created'] = pd.to_datetime(entities['created'])
    
    else:
        # Load pipeline
        nlp = spacy.load("en_core_web_md")

        # Read data file as csv
        rwsb = pd.read_csv("data/reddit_wsb.csv")
        num_posts = len(rwsb)
        print(num_posts)

        # Preprocess some of the column
        rwsb['created'] = pd.to_datetime(rwsb['created'], unit="s")
        print(rwsb)

        entities = []
        
        for post_id, (title, body, created, score) in enumerate(zip(rwsb["title"], rwsb["body"], rwsb["created"], rwsb["score"])):
            # Get text
            if (str(body) == "nan"):
                # If there is no body, the text is only the title.
                text = title
            else:
                # Otherwise we concatenate the title and body.
                text = f"{title} {body}"
            
            # Get entities
            entities_in_post = set()
            doc = nlp(text)
            for ent in doc.ents:
                key = ent.text

                # Only consider entity if its label is relevant for us
                if (str(ent.label_) in {"DATE", "PERCENT", "QUANTITY", "TIME", "WORK_OF_ART", "CARDINAL", "MONEY", "NORP"}):
                    continue

                # Add the entity
                if (key not in entities_in_post):
                    entities_in_post.add(key)
                    entities.append((
                        post_id,
                        created,
                        ent.text,
                        score
                        ))
                    
            # Verbosity
            if (post_id % 500 == 0):
                print(f"{post_id} / {num_posts}")

        # Add to pandas dataframe and save as .csv
        entities = pd.DataFrame(entities, columns=["post_id", "created", "text", "score"])
        entities.to_csv("preprocessed/entities.csv")

    return entities

if __name__ == "__main__":
    gen_entities()