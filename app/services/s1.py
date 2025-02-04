# here s1 means fast thinking
# we will use redis + elasticsearch to cache the result
# previous asked.

import hashlib
import time

import nltk
from elasticsearch import Elasticsearch
from redis import Redis

try:
    # perhaps need to move it to main.py
    # so it will download at start up
    # explicitly download punkt tokenizer
    before = time.time()
    nltk.download("punkt_tab")
    after = time.time()
    print(f"Downloaded punkt in {after - before} seconds.")
except:
    pass


def extract_labels(query: str):
    tokens = nltk.word_tokenize(query.lower())
    labels = [token for token in tokens if token.isalpha()]  # Simple filter
    return labels


class S1:
    def __init__(self, redis: Redis, es: Elasticsearch, es_index: str):
        self.r = redis
        self.es = es
        self.es_index = es_index

    def get_answer_key_from_es(self, labels):
        query = {
            "query": {
                "bool": {"should": [{"match": {"labels": label}} for label in labels]}
            }
        }
        response = self.es.search(index=self.es_index, body=query)
        hits = response["hits"]["hits"]
        if hits:
            return hits[0]["_source"]["answer_id"]  # Assuming the first hit is relevant

    def get_answer(self, query):
        labels = extract_labels(query)
        answer_key_in_redis = self.get_answer_key_from_es(labels)

        if answer_key_in_redis:
            cached_answer = self.r.get(answer_key_in_redis)
            if cached_answer:
                return cached_answer.decode()
        return None

    def store_answer(self, query: str, computed_answer: str, labels: list[str]):
        # No matching answer ID, process and cache new answer
        new_answer_id = hashlib.sha256(query.encode()).hexdigest()
        self.r.set(new_answer_id, computed_answer)
        # Index in Elasticsearch
        self.es.index(
            index=self.es_index, body={"answer_id": new_answer_id, "labels": labels}
        )
        return computed_answer
