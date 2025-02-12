# test_s1.py

import pytest
from app.services.s1 import S1, extract_labels

def test_0_clean_up_redis_and_es(s1: S1):
    print("\n[TEST] Cleaning up Redis and Elasticsearch...")
    s1.r.flushall()
    s1.es.options(ignore_status=[400, 404]).indices.delete(index=s1.es_index)
    print("[TEST] Clean-up complete!")


def test_extract_labels():
    print("\n[TEST] Running test_extract_labels...")

    queries = [
        "What is the capital of France?",
        "你叫什么名字",
        "I visited New York last summer",
    ]

    for q in queries:
        labels = extract_labels(q)
        print(f"Query: {q} -> Extracted Labels: {labels}")


def test_s1_store_answer(s1: S1):
    query, computed_answer = "What is the capital of France?", "Paris"
    print(f"\n[TEST] Storing: '{query}' -> '{computed_answer}'")
    s1.store_answer(query, computed_answer)
    print("[TEST] Stored successfully!")


def test_s1_get_answer(s1: S1):
    print("\n[TEST] Running test_s1_get_answer...")

    queries = ["France capitol is What?", "France capitol what"]
    for query in queries:
        answer = s1.get_answer(query)
        print(f"Query: {query} -> Retrieved Answer: {answer}")
        assert answer == "Paris", f"Expected 'Paris', got '{answer}'"


def test_s1_store_multiple_answers(s1: S1):
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
    print("\n[TEST] Running test_s1_get_answer_none...")

    queries = ["How to cook a puffer fish safely?", "Explain quantum entanglement in detail"]
    for query in queries:
        answer = s1.get_answer(query)
        print(f"Query: {query} -> Retrieved Answer: {answer}")
        assert answer is None, f"Expected None, got '{answer}'"


def test_s1_get_answer_threshold_case(s1: S1):
    print("\n[TEST] Running test_s1_get_answer_threshold_case...")

    query = "Germany city is?"
    answer = s1.get_answer(query)
    print(f"Query: {query} -> Retrieved Answer: {answer}")

    # No assertion here, manually inspect the result
