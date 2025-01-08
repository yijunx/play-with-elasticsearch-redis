
import redis
from elasticsearch import Elasticsearch


# i am quite lazy, i am going to put all secrets here
# anyway everything is local
# commit to git is not a problem
def get_redis_client() -> redis.Redis:
    return redis.Redis(
        host="redis",
        port=6379,
        username="default",
        password="sOmE_sEcUrE_pAsS",
        db=0,
    )

def get_es_client() -> Elasticsearch:
    return Elasticsearch(
        hosts=["http://elasticsearch:9200"])


    






# def process_query(query):
#     # Step 1: Find cache_id from Elasticsearch
#     cache_id = find_cache_id(query)
#     if cache_id:
#         # Step 2: Check Redis for the cached response
#         redis_key = f"cache:{cache_id}"
#         cached_response = redis_client.get(redis_key)
#         if cached_response:
#             return cached_response

#     # Step 3: Fallback to RAG
#     response = generate_response_with_rag(query)
    
#     # Step 4: Cache the response
#     cache_id = generate_unique_cache_id(query)  # Generate a unique ID
#     redis_key = f"cache:{cache_id}"
#     redis_client.set(redis_key, response)
    
#     # Step 5: Update Elasticsearch
#     es_body = {
#         "cache_id": cache_id,
#         "query": query,
#         "tokens": tokenize_query(query),
#     }
#     es_client.index(index="query_labels", body=es_body)

#     return response