from app.services.s1 import S1, extract_labels

def test_0_clean_up_redis_and_es(s1: S1):
    # Clean up Redis and Elasticsearch before running tests
    s1.r.flushall()
    s1.es.options(ignore_status=[400, 404]).indices.delete(index=s1.es_index)


def test_extract_labels():
    # Basic tests for label extraction
    q = "What is the capital of France?"
    labels = extract_labels(q)
    print("Labels for English query:", labels)

    q = "你叫森么名"
    labels = extract_labels(q)
    print("Labels for Chinese query:", labels)


def test_s1_store_answer(s1: S1):
    query = "What is the capital of France?"
    computed_answer = "Paris"
    s1.store_answer(query, computed_answer)


def test_s1_get_answer(s1: S1):
    # Retrieval with slightly rephrased queries
    query = "France capitol is What?"
    answer = s1.get_answer(query)
    assert answer == "Paris", f"Expected 'Paris', got '{answer}'"

    query = "France capitol what"
    answer = s1.get_answer(query)
    assert answer == "Paris", f"Expected 'Paris', got '{answer}'"

