import spacy
import time
from nltk import word_tokenize

# 定义不同的 spaCy NLP 模型（确保已安装）
models = {
    "Small Model (en_core_web_sm)": "en_core_web_sm",
    "Medium Model (en_core_web_md)": "en_core_web_md",
    "Large Model (en_core_web_lg)": "en_core_web_lg",
    "Transformer Model (en_core_web_trf)": "en_core_web_trf"
}

# 定义不同难度的测试文本
test_queries = {
    "Short Text (Simple)": "Apple is a technology company.",
    "Medium Text (More Entities)": "In 2008, Barack Obama was elected as the 44th President of the United States.",
    "Long Text (Complex Sentence)": "SpaceX, led by Elon Musk, successfully launched the Falcon Heavy rocket, carrying a Tesla Roadster as a test payload, marking a significant milestone in private space exploration.",
    "Misspelled Text": "Albert Eintin is famos for his thoery of reltivity.",
    "Ambiguous Expression": "The leading smartphone brand just announced a revolutionary AI-powered device."
}


# 处理函数
def extract_labels(query: str, model_name: str):
    try:
        # 加载指定的 spaCy 模型
        _nlp = spacy.load(model_name)

        start_time = time.time()  # 记录开始时间
        doc = _nlp(query.lower())  # 处理文本
        
        # 提取命名实体
        ent_list = [ent.text for ent in doc.ents]

        # 如果没有识别到命名实体，则进行词语提取
        if not ent_list:
            tokens = word_tokenize(query)
            ent_list = [token for token in tokens if token.isalpha()]

        end_time = time.time()  # 记录结束时间
        elapsed_time = end_time - start_time  # 计算执行时间

        return ent_list, elapsed_time

    except Exception as e:
        return str(e), "Error"

# 运行所有模型和测试文本
results = {}
for text_desc, query in test_queries.items():
    print(f"\n### {text_desc} ###")
    for model_desc, model_name in models.items():
        entities, exec_time = extract_labels(query, model_name)
        results[(text_desc, model_desc)] = (entities, exec_time)
        print(f"--- {model_desc} ---")
        print(f"Extracted Entities: {entities}")
        print(f"Execution Time: {exec_time:.4f} seconds\n")
