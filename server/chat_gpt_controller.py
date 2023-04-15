from flask import Blueprint, request, jsonify
from chat_gpt_service import ChatGptService 
from extensions import *
from models import MessageRequestDTO, HalpreadsBooks
import sqlite3 
import openai
from sklearn.metrics.pairwise import cosine_similarity
import spacy
from typing import List
import pandas as pd 
import pickle
import math 
import numpy as np
import json
import os 
from openai.embeddings_utils import get_embedding, distances_from_embeddings, indices_of_nearest_neighbors_from_distances

openai.api_key = os.getenv('OPENAI_API_KEY')
chat_gpt_route_path = 'chat-gpt-ai'
chat_gpt_route = Blueprint(chat_gpt_route_path, __name__)


# function that generates embeddings from text 
def get_embedding(text, model='text-embedding-ada-002'):
    if isinstance(text, str):
        text = text.replace("\n", " ")
        return openai.Embedding.create(input=[text], model=model)['data'][0]['embedding']
    else:
        return None

df = pd.read_csv('/Users/emilyhalperin/Desktop/halpreads.csv')
conn = sqlite3.connect('instance/app.db')
df.to_sql('halpreads', conn, if_exists='append', index=False)
df['Summary_Embedding'] = df['Summary'].replace("\n", " ").apply(get_embedding)


dfList = []
for index, row in df.iterrows():
    #print(index) #To keep track of which row we are on

    # Create an empty dictionary to store the information for this row
    entry = {}
    entry['Title'] = row['Title']
    entry['Author'] = row['Author']
    entry['Genre'] = row['Genre']
    entry['Rating']= row['Rating']
    entry['Summary'] = row['Summary']
    entry['embedding'] = row['Summary_Embedding']

    # If the 'summary' column is a string and its length is greater than or equal to 33000...
    if isinstance(row['Summary'], str) and len(row['Summary']) >= 33000:
        # ... split the 'summary' value at the first period (.) after the middle of the string and take the second half as the first substring
        embedding1 = openai.Embedding.create(
            input = row['Summary'][row['Summary'].find('.', int (len(row['Summary'])/2))+1:], model="text-embedding-ada-002")['data'][0]['embedding']
        # ... take the first half of the 'summary' value as the second substring
        embedding2 = openai.Embedding.create(
            input = row['Summary'][:row['Summary'].find('.', int (len(row['Summary'])/2))+1], model="text-embedding-ada-002")['data'][0]['embedding']
        # ... set the 'embedding' key in the dictionary to the mean of the embeddings of the two substrings
        entry['embedding'] = np.mean([embedding1, embedding2], axis=0)

    dfList.append(entry)

# Convert dfList to a JSON payload
json_payload = json.dumps(dfList)

query = input("Enter your book title: ")

# Convert query to embedding
query_embedding = openai.Embedding.create(input=query, model="text-embedding-ada-002")['data'][0]['embedding']

# Create a dictionary that maps values
embedding_dict = df.set_index('Title')[['embedding']].to_dict()['embedding']

# Calculate the distances between the query embedding and the summary embeddings using the cosine distance metric
distances = distances_from_embeddings(query_embedding, list(embedding_dict.values()), distance_metric="cosine")

# Get the indices of the nearest neighbors (i.e., the summaries with the smallest distances)
indices_of_nearest_neighbors = indices_of_nearest_neighbors_from_distances(distances)

# Print the titles of the top 5 recommended books
print("Titles of top 5 recommended books:")
print(df.loc[indices_of_nearest_neighbors[:5]]['title'])

# Print the genres of the top 5 recommended books
print("\nGenres of top 5 recommended books:")
print(df.loc[indices_of_nearest_neighbors[:5]]['genre'])

# Function that constructs the prompt
def construct_prompt(query, title, author, summary):
    return f"You are a chatbot that recommends books. A user has asked for a recommendation for a book similar to '{query}'. Please recommend a book similar to '{query}' that the user will enjoy. Write a recommendation for the book '{title}' by {author}. Here is a summary of '{title}': {summary}. Be very descriptive about why you chose this book for the user."

# Get the top recommended book
top_recommendation = df.loc[indices_of_nearest_neighbors[0]]

# Construct the prompt
prompt = construct_prompt(query, top_recommendation['title'], top_recommendation['author'], top_recommendation['summarySpaced'])

# Use the OpenAI text completion API to generate a recommendation based on the prompt
completion = openai.Completion.create(model="text-davinci-003", prompt=prompt, max_tokens=1000, temperature=0, stop=None)

# Print the recommendation
print(completion.text)





@chat_gpt_route.route('/message', methods=['POST'])
def get_ai_model_answer():
    body = request.json
    return jsonify({
        'result': ChatGptService.get_ai_model_answer(MessageRequestDTO.new_instance_from_flask_body(body))
    })