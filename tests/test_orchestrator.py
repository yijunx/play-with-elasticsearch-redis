from app.orchestractor.base import Orchestrator


def test_orchestractor1(orchestractor: Orchestrator):
    query = "where do i buy a gameboy"
    answer = orchestractor.get_answer(query)
    ans2 = orchestractor.get_answer(query)
    assert answer == ans2

def test_orchestractor2(orchestractor: Orchestrator):
    query = "where do i buy a ps4"
    answer = orchestractor.get_answer(query)
    ans2 = orchestractor.get_answer(query)
    assert answer == ans2
