import pytest

import simpleregistry


@pytest.fixture
def my_registry():
    class MyRegistry(simpleregistry.Registry):
        pass

    yield MyRegistry("my_registry")


@pytest.fixture
def MyRegistered(my_registry: simpleregistry.Registry):
    @simpleregistry.register(my_registry)
    class MyRegisteredInner:
        pass

    yield MyRegisteredInner
