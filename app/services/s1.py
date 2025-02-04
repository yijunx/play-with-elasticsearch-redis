# here s1 means fast thinking
# we will use redis + elasticsearch to cache the result
# previous asked.

from redis import Redis
from elasticsearch import Elasticsearch
import hashlib
import nltk
import time

try:
    # perhaps need to move it to main.py
    # so it will download at start up
    # explicitly download punkt tokenizer
    before = time.time()
    nltk.download('punkt_tab')
    after = time.time()
    print(f"Downloaded punkt in {after - before} seconds.")
except:
    pass


def extract_labels(query: str):
    tokens = nltk.word_tokenize(query.lower())
    labels = [token for token in tokens if token.isalpha()]  # Simple filter
    return labels

class S1:
    def __init__(self, redis: Redis, es: Elasticsearch):
        self.r = redis
        self.es = es

    # def get_answer(self, question: str) -> str:

    #     def get_answer_id(labels):
    #         query = {
    #             "query": {
    #                 "bool": {
    #                     "should": [
    #                         {"match": {"labels": label}} for label in labels
    #                     ]
    #                 }
    #             }
    #         }
    #         response = self.es.search(index=ES_INDEX, body=query)
    #         hits = response['hits']['hits']
    #         if hits:
    #             return hits[0]['_source']['answer_id']  # Assuming the first hit is relevant
    #         return None
    #             return "Data from S1"

    #     def get_answer(query):
    #         labels = extract_labels(query)
    #         answer_id = get_answer_id(labels)
            
    #         if answer_id:
    #             cached_answer = r.get(answer_id)
    #             if cached_answer:
    #                 return cached_answer.decode()
    #             else:
    #                 # Simulate computing the answer
    #                 computed_answer = compute_answer(query)
    #                 self.r.set(answer_id, computed_answer)
    #                 return computed_answer
    #         else:
    #             # No matching answer ID, process and cache new answer
    #             computed_answer = compute_answer(query)
    #             new_answer_id = hashlib.sha256(query.encode()).hexdigest()
    #             self.r.set(new_answer_id, computed_answer)
    #             # Index in Elasticsearch
    #             self.es.index(index=ES_INDEX, body={"answer_id": new_answer_id, "labels": labels})
    #             return computed_answer   

    def store_answer(self, question: str, answer: str):
        pass

ES_INDEX = 'answers'

# Step 1: Label Extraction (Simple Tokenization for Demo)


# Step 2: Query Elasticsearch to Get Answer ID


# Step 3: Retrieve from Redis or Compute and Cache


# Simulated Answer Computation
def compute_answer(query):
    if "strawberry" in query and "r" in query:
        return "3"  # Hardcoded for the demo
    return "Answer not available."

# Example Query
# query = "How many R's are in strawberry?"
# print(get_answer(query))