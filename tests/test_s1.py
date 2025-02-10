# test_s1.py

import pytest
from app.services.s1 import S1, extract_labels

def test_0_clean_up_redis_and_es(s1: S1):
    """
    清理 Redis 和 Elasticsearch，确保测试的干净环境
    """
    print("\n[TEST] Cleaning up Redis and Elasticsearch...")
    s1.r.flushall()
    s1.es.options(ignore_status=[400, 404]).indices.delete(index=s1.es_index)
    print("[TEST] Clean-up complete!")


def test_extract_labels():
    """
    测试标签提取功能
    """
    print("\n[TEST] Running test_extract_labels...")

    q = "What is the capital of France?"
    labels = extract_labels(q)
    print(f"Query: {q} -> Extracted Labels: {labels}")

    q = "你叫什么名字"
    labels = extract_labels(q)
    print(f"Query: {q} -> Extracted Labels: {labels}")

    q = "I visited New York last summer"
    labels = extract_labels(q)
    print(f"Query: {q} -> Extracted Labels: {labels}")


def test_s1_store_answer(s1: S1):
    """
    测试向 S1 存储单个问题与答案
    """
    query = "What is the capital of France?"
    computed_answer = "Paris"
    print(f"\n[TEST] Storing: '{query}' -> '{computed_answer}'")
    s1.store_answer(query, computed_answer)
    print("[TEST] Stored successfully!")


def test_s1_get_answer(s1: S1):
    """
    测试用相似问法来检索已存储的答案
    """
    print("\n[TEST] Running test_s1_get_answer...")

    queries = ["France capitol is What?", "France capitol what"]
    for query in queries:
        answer = s1.get_answer(query)
        print(f"Query: {query} -> Retrieved Answer: {answer}")
        assert answer == "Paris", f"Expected 'Paris', got '{answer}'"


def test_s1_store_multiple_answers(s1: S1):
    """
    存储多个问题-答案对到 S1
    """
    print("\n[TEST] Storing multiple QA pairs...")
    qa_pairs = [
        ("What is the capital of Germany?", "Berlin"),
        ("What is the capital of Italy?", "Rome"),
        ("Explain BFS in graph theory", "BFS stands for Breadth-First Search..."),
        ("Which city is known as the Big Apple?", "New York City"),
    ]

    for query, ans in qa_pairs:
        print(f"Storing: '{query}' -> '{ans}'")
        s1.store_answer(query, ans)
    
    print("[TEST] Multiple QA pairs stored successfully!")


def test_s1_get_answer_multiple(s1: S1):
    """
    测试针对多个已存储问题的相似问法检索
    """
    print("\n[TEST] Running test_s1_get_answer_multiple...")

    queries_and_expected = [
        ("the capital city of Germany is what?", "Berlin"),
        ("Can you explain BFS for searching a graph?", "BFS stands for"),
        ("What's Italy's capital?", "Rome"),
        ("What is Big Apple referring to?", "New York City"),
    ]

    for query, expected in queries_and_expected:
        answer = s1.get_answer(query)
        print(f"Query: {query} -> Retrieved Answer: {answer}")
        assert answer and expected in answer, f"Expected '{expected}', but got '{answer}'"


def test_s1_get_answer_none(s1: S1):
    """
    测试无法匹配到答案时，返回 None
    """
    print("\n[TEST] Running test_s1_get_answer_none...")

    queries = ["How to cook a puffer fish safely?", "Explain quantum entanglement in detail"]
    for query in queries:
        answer = s1.get_answer(query)
        print(f"Query: {query} -> Retrieved Answer: {answer}")
        assert answer is None, f"Expected None, got '{answer}'"


def test_s1_get_answer_threshold_case(s1: S1):
    """
    测试相似度边缘案例
    """
    print("\n[TEST] Running test_s1_get_answer_threshold_case...")

    query = "Germany city is?"
    answer = s1.get_answer(query)
    print(f"Query: {query} -> Retrieved Answer: {answer}")

    # 这里不强制断言，可以手动观察
