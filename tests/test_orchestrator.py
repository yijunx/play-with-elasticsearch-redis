from app.orchestractor.base import Orchestrator


def test_orchestractor1(orchestractor: Orchestrator):
    query = "can you tell me what Gameboy can do"
    answer = orchestractor.get_answer(query)
    ans2 = orchestractor.get_answer(query)
    assert answer == ans2

def test_orchestractor2(orchestractor: Orchestrator):
    query = "can you tell me what PS4 can do"
    answer = orchestractor.get_answer(query)
    ans2 = orchestractor.get_answer(query)
    assert answer == ans2

# def test_orchestractor1(orchestractor: Orchestrator):
#     query = "help me make a 7-days travel plan for Nanjing"
#     answer = orchestractor.get_answer(query)
#     ans2 = orchestractor.get_answer(query)
#     assert answer == ans2

# def test_orchestractor2(orchestractor: Orchestrator):
#     query = "Help me pln a one-week trip to Najing"
#     answer = orchestractor.get_answer(query)
#     ans2 = orchestractor.get_answer(query)
#     assert answer == ans2