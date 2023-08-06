import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from openai.embeddings_utils import get_embedding

def construct_ws_dataframe():
    df = pd.DataFrame(columns=["text", "vector_embedding"])
    return df


def embed(text):
    embedding_model = "text-embedding-ada-002"
    return get_embedding(text, engine=embedding_model)

def insert_embedding_to_def(df, text):
    df.loc[len(df)] = {"text": text, "vector_embedding": embed(text)}
    return df

def wip_add_to_df(df):
    df = insert_embedding_to_def(df, "The wine from the party in winter of 2016 had a picture of a dragon on the label. Eric said it was expensive.")
    df = insert_embedding_to_def(df, "This wine was from 2018 and had a green label. It was okay, but Ive had better")
    df = insert_embedding_to_def(df, "The merlot from the San Carlos diner is really great. It is a Chateau de Saund 2017. It paired really nicely with the fish")
    return df


def vector_similarity(df, text):

    vec = embed(text)
    df["similarity"] = df["vector_embedding"].apply(lambda x: cosine_similarity([x], [vec]))
    df = df.sort_values(by=["similarity"], ascending=False).reset_index()
    # print(df)
    return df.loc[0]


def retrieve(df, text):
    most_relevant = vector_similarity(df, text)
    print(f"You asked for: {text}")
    print(f"The most relevent entry is: {most_relevant['text']}")
    print()

if __name__ == "__main__":
    ws_df = construct_ws_dataframe()
    wip_add_to_df(ws_df)
    retrieve(ws_df, "I want the wine with the dragon label")
    retrieve(ws_df, "What was the wine I had from Chateau de Saund?")
    retrieve(ws_df, "I went to the San Carlos diner and had a great wine. What was it?")
    retrieve(ws_df, "Laura said some wine was really expensive. Or maybe it was Eric.")
