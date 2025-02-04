from app.services.s1 import S1, extract_labels


def test_extract_labels():
    q = "What is the capital of France?"
    labels = extract_labels(q)
    print(labels)

    q = "你叫森么名"
    labels = extract_labels(q)
    print(labels)


def test_s1_store_answer(s1: S1):
    query = "What is the capital of France?"
    computed_answer = "Paris"
    labels = extract_labels(query)
    print(labels)
    s1.store_answer(query, computed_answer, labels)


def test_s1_get_answer(s1: S1):
    query = "France capitol is What?"
    answer = s1.get_answer(query)
    assert answer == "Paris"

    query = "France capitol what"
    answer = s1.get_answer(query)
    assert answer == "Paris"
