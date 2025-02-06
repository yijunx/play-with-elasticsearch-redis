import hashlib
import time

import nltk
from elasticsearch import Elasticsearch
from redis import Redis

import spacy
from spacy.tokens import Doc
from nltk import word_tokenize

try:
    before = time.time()
    nltk.download("punkt_tab")
    after = time.time()
    print(f"Downloaded punkt in {after - before} seconds.")
except:
    pass

# --------------- NER + labels ---------------------
def setup_spacy_nlp():
      
    #   poetry add spacy
    #   python -m spacy download en_core_web_sm

    return spacy.load("en_core_web_sm")


_nlp = spacy.load("en_core_web_sm")


def extract_labels(query: str):
    doc = _nlp(query.lower())

    # PRODUCT (商品), ORG (组织), GPE (地理政治实体)
    # For more detailed classification, we can use spaCy's en_core_web_trf (Transformer-based) model

    ent_list = [ent.text for ent in doc.ents if ent.label_ in ["PRODUCT", "ORG", "GPE"]]

    if not ent_list:
        tokens = word_tokenize(query)
        ent_list = [token for token in tokens if token.isalpha()]

    return ent_list


class S1:
    def __init__(self, redis: Redis, es: Elasticsearch, es_index: str):
        self.r = redis
        self.es = es
        self.es_index = es_index
        self.nlp = _nlp

    def get_answer_key_from_es(self, labels):
        should_clauses = [
            {"match": {"labels": {"query": label, "fuzziness": "AUTO"}}}
            for label in labels
        ]

        query = {
            "query": {
                "bool": {
                    "should": should_clauses,
                    "minimum_should_match": 1
                }
            }
        }

        response = self.es.search(index=self.es_index, body=query)
        hits = response["hits"]["hits"]

        if hits:
            return hits[0]["_source"]["answer_id"]
        return None


    def get_answer(self, query: str):
        labels = extract_labels(query)
        answer_key_in_redis = self.get_answer_key_from_es(labels)

        if answer_key_in_redis:
            cached_answer = self.r.get(answer_key_in_redis)
            if cached_answer:
                return cached_answer.decode()
        return None

    def store_answer(self, query: str, computed_answer: str):
        labels = extract_labels(query)
        new_answer_id = hashlib.sha256(query.encode()).hexdigest()

        self.r.set(new_answer_id, computed_answer)

        doc = {
            "answer_id": new_answer_id,
            "labels": labels,
        }
        self.es.index(index=self.es_index, body=doc)

        self.es.indices.refresh(index=self.es_index)

        return computed_answer
