import pytest
from elasticsearch import Elasticsearch
from redis import Redis

from app.context_providers.base_context_provider import JiberishContextProvider
from app.llm.basic_llm import BasicLLM
from app.main import (
    get_context_provider_one,
    get_context_provider_two,
    get_es,
    get_llm,
    get_orchestrator,
    get_r,
    get_s1,
    get_s2,
)
from app.services.s1 import S1
from app.services.s2 import S2
from app.utils.config import env


@pytest.fixture
def context_provider_one():
    return get_context_provider_one()


@pytest.fixture
def context_provider_two():
    return get_context_provider_two()


@pytest.fixture
def llm():
    return get_llm()


@pytest.fixture
def r():
    return get_r()


@pytest.fixture
def es():
    return get_es()


@pytest.fixture
def s2():
    return get_s2()


@pytest.fixture
def s1():
    return get_s1()


@pytest.fixture
def orchestrator():
    return get_orchestrator()