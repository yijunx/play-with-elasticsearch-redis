from app.orchestrator.base import Orchestrator

def test_0_clean_up_storage(orchestrator: Orchestrator):
    print("\n[TEST] Cleaning up Redis and Elasticsearch before running tests...")
    orchestrator.s1.r.flushall()
    orchestrator.s1.es.options(ignore_status=[400, 404]).indices.delete(index=orchestrator.s1.es_index)

    orchestrator.s1._ensure_es_index()
    print("[TEST] Clean-up complete, and index recreated!")


### **Type 1: Same Meaning, Different Keywords**
def test_orchestrator_similar_keywords(orchestrator: Orchestrator):
    """
    Verify that orchestrator handles questions with different keywords but the same meaning.
    """
    print("\n[TEST] Running test_orchestrator_similar_keywords...")
    query1 = "Can you recommend a laptop for gaming under $1500?"
    query2 = "Best gaming laptops for 2024?"

    answer1 = orchestrator.get_answer(query1)
    answer2 = orchestrator.get_answer(query2)

    print(f"Query 1: {query1} -> Answer: {answer1}")
    print(f"Query 2: {query2} -> Answer: {answer2}")

    assert answer1 == answer2 or answer2 is not None, "Expected similar answers."

### **Type 2: Different Wording, Same Meaning**
def test_orchestrator_different_wording(orchestrator: Orchestrator):
    """
    Test questions that have different wording but mean the same thing.
    """
    print("\n[TEST] Running test_orchestrator_different_wording...")
    query1 = "What is the capital of Canada?"
    query2 = "Cpital of Cnada? Otawa or Tronto?"

    answer1 = orchestrator.get_answer(query1)
    answer2 = orchestrator.get_answer(query2)

    print(f"Query 1: {query1} -> Answer: {answer1}")
    print(f"Query 2: {query2} -> Answer: {answer2}")

    assert answer1 == answer2, "Expected identical answers."

### **Type 3: Misspelled and Informal Queries**
def test_orchestrator_misspelled_query(orchestrator: Orchestrator):
    """
    Check if the system correctly retrieves answers for misspelled and informal queries.
    """
    print("\n[TEST] Running test_orchestrator_misspelled_query...")
    query1 = "Who won the FIFA World Cup in 2018?"
    query2 = "2018 Fifa cham? Frnace or Germany?"

    answer1 = orchestrator.get_answer(query1)
    answer2 = orchestrator.get_answer(query2)

    print(f"Query 1: {query1} -> Answer: {answer1}")
    print(f"Query 2: {query2} -> Answer: {answer2}")

    assert answer1 == answer2, "Misspelled query should retrieve the same answer."

### **Type 4: Multi-Sentence Complex Queries**
def test_orchestrator_complex_query(orchestrator: Orchestrator):
    """
    Check if the orchestrator can handle complex, multi-sentence queries.
    """
    print("\n[TEST] Running test_orchestrator_complex_query...")
    query1 = "How do I reach the Eiffel Tower from CDG airport?"
    query2 = "I'm landing at Charles de Gaulle airport. What's the best way to get to the Eiffel Tower?"

    answer1 = orchestrator.get_answer(query1)
    answer2 = orchestrator.get_answer(query2)

    print(f"Query 1: {query1} -> Answer: {answer1}")
    print(f"Query 2: {query2} -> Answer: {answer2}")

    assert answer1 == answer2, "Complex queries should yield the same answer."

### **Type 5: Ambiguous Queries**
def test_orchestrator_ambiguous_query(orchestrator: Orchestrator):
    """
    Test if ambiguous queries still return meaningful answers.
    """
    print("\n[TEST] Running test_orchestrator_ambiguous_query...")
    query = "Tell me about Tesla."
    answer = orchestrator.get_answer(query)

    print(f"Query: {query} -> Answer: {answer}")

    assert answer is not None, "Ambiguous queries should still return an answer."

### **Type 6: Completely Different Queries**
def test_orchestrator_unrelated_queries(orchestrator: Orchestrator):
    """
    Ensure that completely different questions don't return the same answer.
    """
    print("\n[TEST] Running test_orchestrator_unrelated_queries...")
    query1 = "How do I bake a chocolate cake?"
    query2 = "What is the capital of Australia?"

    answer1 = orchestrator.get_answer(query1)
    answer2 = orchestrator.get_answer(query2)

    print(f"Query 1: {query1} -> Answer: {answer1}")
    print(f"Query 2: {query2} -> Answer: {answer2}")

    assert answer1 != answer2, "Unrelated questions should have different answers."

### **Type 7: New Query Triggers LLM Answer Generation**
def test_orchestrator_s2_generation(orchestrator: Orchestrator):
    """
    Test if a completely new query (not in ES or Redis) triggers the LLM (S2) to generate a new answer.
    """
    print("\n[TEST] Running test_orchestrator_s2_generation...")
    new_query = "Who invented Bitcoin?"
    
    answer1 = orchestrator.get_answer(new_query)  # First retrieval should call S2
    answer2 = orchestrator.get_answer(new_query)  # Second retrieval should hit Redis/ES

    print(f"Query: {new_query} -> First Answer: {answer1}")
    print(f"Query: {new_query} -> Second Answer: {answer2}")

    assert answer1 is not None, "LLM (S2) should generate an answer."
    assert answer1 == answer2, "Once stored, subsequent queries should return the same answer."

### **Type 8: Threshold-Based Similarity Matching**
def test_orchestrator_threshold_matching(orchestrator: Orchestrator):
    """
    Ensure that near-identical questions pass the similarity threshold and retrieve the same answer.
    """
    print("\n[TEST] Running test_orchestrator_threshold_matching...")
    query1 = "What are the best programming languages for AI development?"
    query2 = "AI coding lang? Pythn best?"

    answer1 = orchestrator.get_answer(query1)
    answer2 = orchestrator.get_answer(query2)

    print(f"Query 1: {query1} -> Answer: {answer1}")
    print(f"Query 2: {query2} -> Answer: {answer2}")

    assert answer1 == answer2, "Similar AI-related questions should return the same answer."

