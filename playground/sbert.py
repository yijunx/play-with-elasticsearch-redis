from sentence_transformers import SentenceTransformer, util

def compute_similarity(sentence1: str, sentence2: str):
    # 加载 SBERT 预训练模型
    model = SentenceTransformer("all-MiniLM-L6-v2")

    # 计算句子嵌入
    embedding1 = model.encode(sentence1, convert_to_tensor=True)
    embedding2 = model.encode(sentence2, convert_to_tensor=True)

    # 计算余弦相似度
    similarity = util.pytorch_cos_sim(embedding1, embedding2)

    return similarity.item()

if __name__ == "__main__":
    sentence1 = "I love programming."
    sentence2 = "Coding is my passion."

    similarity = compute_similarity(sentence1, sentence2)
    print(f"Sentence Similarity: {similarity:.4f}")
