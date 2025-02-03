from app.services.s2 import S2


def test_s2(s2: S2):
    print(s2.get_answer(question="what lunch should I get"))
