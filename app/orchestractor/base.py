from app.services.s1 import S1, extract_labels
from app.services.s2 import S2


class Orchestrator:
    def __init__(self, s1: S1, s2: S2):
        self.s1 = s1
        self.s2 = s2

    def get_answer(self, query: str):
        print("###### we are in the orchestrator ######")

        ans = self.s1.get_answer(query)
        if ans:
            print("###### answer from s1 ######")
            print("ans: ", ans)
            return ans
        
        else:
            ans = self.s2.get_answer(query)
            labels = extract_labels(query)
            self.s1.store_answer(query, ans)
            print("###### answer from s2 ######")
            print("ans: ", ans)
            return ans
