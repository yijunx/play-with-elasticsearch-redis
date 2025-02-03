# here s2 means the system2 thinking
# in actual implementation, it means make use of the context provider
# and llm to create a well-thought answer
# but here i will make it real simple

import asyncio

from app.context_providers.base_context_provider import (
    BaseContextProvider,
    gather_async_contexts,
)
from app.llm.basic_llm import BasicLLM


def mock_embeddings(sentence: str) -> list[float]:
    return [0.0] * 512


class s2:
    def __init__(self, llm: BasicLLM, context_providers: list[BaseContextProvider]):
        self.llm = llm
        self.context_providers = context_providers

    def get_answer(self, question: str):

        contexts = asyncio.run(
            gather_async_contexts(
                async_providers=self.context_providers,
                n=5,
                query_vector=mock_embeddings(question),
            )
        )
