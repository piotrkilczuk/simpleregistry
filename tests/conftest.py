import pytest

import simpleregistry


@pytest.fixture
def my_registry():
    class MyRegistry(simpleregistry.Registry):
        pass

    yield MyRegistry("my_registry")


@pytest.fixture
def MyRegistered(my_registry: simpleregistry.Registry):
    class MyRegisteredInner(simpleregistry.Registered):
        class Config(simpleregistry.PyregConfig):
            registry = my_registry

    yield MyRegisteredInner
