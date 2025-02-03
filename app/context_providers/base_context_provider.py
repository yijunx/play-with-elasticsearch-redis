import asyncio
from abc import ABC, abstractmethod


class BaseContextProvider(ABC):
    def __init__(self, quantity_chunks_retrieved: int = None):
        self.chunks_retrieved = (
            quantity_chunks_retrieved if quantity_chunks_retrieved else 5
        )

    @abstractmethod
    async def provide_contexts(
        self, query_vector: list[float], quantity: int
    ) -> list[str]: ...


class JiberishContextProvider(BaseContextProvider):
    def __init__(self, facts: list[str], simulated_delay: int = 0):
        self.simulated_delay = simulated_delay
        self.facts = facts

    async def provide_contexts(
        self, query_vector: list[float], quantity: int
    ) -> list[str]:
        await asyncio.sleep(self.simulated_delay)
        return self.facts[:quantity]


async def gather_async_contexts(
    async_providers: list[BaseContextProvider], n: int, query_vector: list[float]
) -> list[list[str]]:
    tasks = [
        provider.provide_contexts(query_vector=[0.0] * 512, quantity=n)
        for provider in async_providers
    ]
    results = await asyncio.gather(*[task for task in tasks])
    return results


# class AsyncContextProvider1(BaseContextProvider):
#     async def provide_contexts(
#         self, query_vector: list[float], query: str
#     ) -> list[str]:
#         tasks = [
#             asyncio.sleep(5),
#             asyncio.sleep(5),
#         ]
#         results = await asyncio.gather(*[task for task in tasks])
#         return []


# class AsyncContextProvider2(BaseContextProvider):
#     async def provide_contexts(
#         self, query_vector: list[float], query: str
#     ) -> list[str]:
#         tasks = [
#             asyncio.sleep(5),
#             asyncio.sleep(5),
#         ]
#         results = await asyncio.gather(*[task for task in tasks])
#         return []
