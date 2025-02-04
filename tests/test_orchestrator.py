from app.orchestractor.base import Orchestrator


def test_orchestractor(orchestractor: Orchestrator):
    query = "where do i buy a gameboy"
    answer = orchestractor.get_answer(query)
    ans2 = orchestractor.get_answer(query)
    assert answer == ans2
