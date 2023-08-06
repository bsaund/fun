"""
This is a quick look at using vector embeddings to match input data with queries.
To use this, you will set to set your environment variable for the openAI key
https://github.com/openai/openai-python#usage
"""

import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from openai.embeddings_utils import get_embedding

ENTRIES = [
"The wine from the party in winter of 2016 had a picture of a dragon on the label. Eric said it was expensive.",
"This wine was from 2018 and had a green label. It was okay, but Ive had better",
"The merlot from the San Carlos diner is really great. It is a Chateau de Saund 2017. It paired really nicely with the fish",
"The pinot noir from the San Carlos diner is awful. It is a Chateu de Cochran 1956. Never get this again"
]

QUERIES = [
"I want the wine with the dragon label",
"What was the wine I had from Chateau de Saund?",
"I went to the San Carlos diner and had a great wine. What was it?",
"Laura said some wine was really expensive. Or maybe it was Eric.",
"I had a terrible wine at the San Carlos diner from some Chateu. What was it?"
]

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
    for entry in ENTRIES:
        df = insert_embedding_to_def(df, entry)
    return df


def vector_similarity(df, text):

    vec = embed(text)
    df["similarity"] = df["vector_embedding"].apply(lambda x: cosine_similarity([x], [vec]))
    df = df.sort_values(by=["similarity"], ascending=False).reset_index()
    return df.loc[0]


def retrieve(df, text):
    most_relevant = vector_similarity(df, text)
    print(f"You asked for    :   {text}")
    print(f"The best entry is:   {most_relevant['text']}")
    print()

if __name__ == "__main__":
    ws_df = construct_ws_dataframe()
    wip_add_to_df(ws_df)
    for query in QUERIES:
        retrieve(ws_df, query)
