import hashlib
import time
import json

import nltk
from elasticsearch import Elasticsearch
from redis import Redis

import spacy
from spacy.tokens import Doc
from nltk import word_tokenize

from sentence_transformers import SentenceTransformer
import numpy as np

try:
    before = time.time()
    nltk.download("punkt")
    after = time.time()
    print(f"Downloaded punkt in {after - before} seconds.")
except:
    pass

_nlp = spacy.load("en_core_web_trf")
_embedding_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

def cosine_similarity(vec_a, vec_b):
    return np.dot(vec_a, vec_b) / (np.linalg.norm(vec_a) * np.linalg.norm(vec_b))


def extract_labels(query: str):
    doc = _nlp(query.lower())
    ent_list = [ent.text for ent in doc.ents]

    if not ent_list:
        tokens = word_tokenize(query)
        ent_list = [token for token in tokens if token.isalpha()]

    return ent_list


class S1:
    def __init__(self, redis: Redis, es: Elasticsearch, es_index: str):
        self.r = redis
        self.es = es
        self.es_index = es_index
        self._ensure_es_index()
        self.nlp = _nlp
        self.embedding_model = _embedding_model


    # Ensures the Elasticsearch index exists
    def _ensure_es_index(self):
        if not self.es.indices.exists(index=self.es_index):
            print(f"[INFO] Index '{self.es_index}' not found, creating it...")
            self.es.indices.create(index=self.es_index, body={
                "settings": {
                    "number_of_shards": 1,
                    "number_of_replicas": 1
                },
                "mappings": {
                    "properties": {
                        "answer_id": {"type": "keyword"},
                        "labels": {"type": "text"},
                        "question": {"type": "text"}
                    }
                }
            })
            print(f"[INFO] Index '{self.es_index}' created successfully.")


    def _get_candidate_docs_from_es(self, labels):
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
        return hits


    # Retrieves an answer based on query similarity
    def get_answer(self, query: str):
        labels = extract_labels(query)

        candidate_docs = self._get_candidate_docs_from_es(labels)
        if not candidate_docs:
            return None

        query_emb = self.embedding_model.encode(query)

        best_match_answer = None
        best_similarity = -1.0

        for doc in candidate_docs:
            source = doc["_source"]
            answer_id = source["answer_id"]
            
            candidate_data = self.r.get(answer_id)
            if not candidate_data:
                continue
            
            candidate_json = json.loads(candidate_data.decode("utf-8"))
            candidate_query = candidate_json["question"]
            candidate_answer = candidate_json["answer"]
            candidate_emb = np.array(candidate_json["question_embedding"], dtype=float)

            sim = cosine_similarity(query_emb, candidate_emb)
            if sim > best_similarity:
                best_similarity = sim
                best_match_answer = candidate_answer

        SIMILARITY_THRESHOLD = 0.3
        if best_similarity >= SIMILARITY_THRESHOLD:
            return best_match_answer
        else:
            return None


    def store_answer(self, query: str, computed_answer: str):
        labels = extract_labels(query)
        new_answer_id = hashlib.sha256(query.encode()).hexdigest()

        query_emb = self.embedding_model.encode(query).tolist()

        redis_record = {
            "question": query,
            "labels": labels,
            "answer": computed_answer,
            "question_embedding": query_emb
        }

        self.r.set(new_answer_id, json.dumps(redis_record))

        doc = {
            "answer_id": new_answer_id,
            "labels": labels,
            "question": query
        }
        self.es.index(index=self.es_index, body=doc)
        self.es.indices.refresh(index=self.es_index)

        return computed_answer
