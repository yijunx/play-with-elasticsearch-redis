from sentence_transformers import SentenceTransformer

_embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

query = "Apple is a technology company."
query_emb = _embedding_model.encode(query).tolist()

print(query_emb)