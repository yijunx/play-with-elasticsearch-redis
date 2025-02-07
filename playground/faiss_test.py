import time
import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
import os

file_path = os.path.abspath("./playground/test_cases.json")
print(f"Using file path: {file_path}")  # 这将打印文件的绝对路径

with open(file_path, "r", encoding="utf-8") as file:
    test_data = json.load(file)["test_cases"]


# 定义不同的 SBERT 模型
models = {
    "MiniLM (all-MiniLM-L6-v2)": "all-MiniLM-L6-v2",
    "MPNet (all-mpnet-base-v2)": "all-mpnet-base-v2",
    "STSB RoBERTa (stsb-roberta-large)": "stsb-roberta-large",
    "Multilingual MiniLM (paraphrase-multilingual-MiniLM-L12-v2)": "paraphrase-multilingual-MiniLM-L12-v2"
}

# 记录所有测试结果
all_results = {}

# 遍历所有测试组
for i, test_case in enumerate(test_data, 1):
    question_bank = test_case["question_bank"]
    query_text = test_case["query_text"]

    print(f"\n==== Running Test Case {i}: {query_text} ====\n")

    # 记录当前测试组的结果
    test_case_results = {}

    for model_desc, model_name in models.items():
        # 1. 加载模型
        model = SentenceTransformer(model_name)

        # 2. 计算所有问题的嵌入
        start_time = time.time()
        question_embeddings = model.encode(question_bank)
        index = faiss.IndexFlatL2(question_embeddings.shape[1])  # L2 距离索引
        index.add(np.array(question_embeddings))

        # 3. 计算查询句子的嵌入
        query_embedding = model.encode([query_text])

        # 4. 搜索最近的匹配问题
        D, I = index.search(np.array(query_embedding), 1)  # 找到最近的 1 个问题
        end_time = time.time()

        # 5. 记录执行时间和最匹配的问题
        matched_question = question_bank[I[0][0]]
        execution_time = (end_time - start_time) * 1000

        test_case_results[model_desc] = {
            "Matched Question": matched_question,
            "Similarity Score": round(float(D[0][0]), 4),
            "Execution Time (ms)": execution_time
        }

        print(f"\n--- {model_desc} ---")
        print(f"Matched Question: {matched_question}")
        print(f"Similarity Score: {D[0][0]}")
        print(f"Execution Time: {execution_time:.2f} ms")

    # 保存当前测试组的结果
    all_results[f"Test Case {i}"] = test_case_results

# 输出最终结果（如果需要保存到 JSON，可以启用）
with open("./playground/test_results.json", "w", encoding="utf-8") as result_file:
    json.dump(all_results, result_file, indent=4, ensure_ascii=False)

print("\n==== All Test Cases Completed! Results saved to 'test_results.json' ====")
