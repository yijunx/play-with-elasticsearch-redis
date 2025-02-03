# here s1 means fast thinking
# we will use redis + elasticsearch to cache the result
# previous asked.
from redis import Redis
from elasticsearch import Elasticsearch


class S1:
    def __init__(self, redis: Redis, es: Elasticsearch):
        self.redis = redis
        self.es = es

    # raise when there is no answer
    def get_answer(self, question: str) -> str:
        return "Data from S1"
    

    def store_answer(self, question: str, answer: str):
        pass
    