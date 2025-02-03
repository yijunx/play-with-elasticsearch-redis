# play-with-elasticsearch-redis
for cache layer before go into weaviate


Some technical details regarding redis + elasticsearch: (need to verify, find out the best way to use it, to save our token usage to reduce gpu burden or $ cost)
You can start by asking chatgpt:
i want to use redis and elastic search the cache the result from queries. before redis and elastic search, i have use rag with LLM and vector db. i also want to enable that, there is segregation in redis for each user (i cannot get cache for Alice even if Alice asked same question, there might be privacy issue). how should I do?
but user may vary the query even if it is asking the same thing. how about let redis have a key, and the key has a mapping label in elasticsearch, when the query comes, somehow i turn the query into label, and get the key back from elasticsearch. how do i do this? is this similar to inverted index?
when do I do cache invalidation? any good suggestions?
could you elaborate on the preprocess? 
how do I get the tokens into elasticsearch? and then next query comes, how do i take the new token from this query then get the catch_id from elasticsearch?