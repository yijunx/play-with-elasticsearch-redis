from app.services.s1 import S1, extract_labels


def test_extract_labels():
    q = "What is the capital of France?"
    labels = extract_labels(q)
    print(labels)

    q = "你叫森么名"
    labels = extract_labels(q)
    print(labels)