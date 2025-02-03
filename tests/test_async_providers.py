import asyncio

from app.context_providers.base_context_provider import (
    BaseContextProvider,
    gather_async_contexts,
)


def test_gather_contexts(
    context_provider_one: BaseContextProvider,
    context_provider_two: BaseContextProvider,
):
    contexts = asyncio.run(
        gather_async_contexts(
            async_providers=[context_provider_one, context_provider_two],
            n=1,
            # does not matter
            query_vector=[0.0] * 512,
        )
    )
    print(contexts)
