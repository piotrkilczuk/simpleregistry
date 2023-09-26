import pytest

import pyreg


@pytest.fixture
def my_registry():
    class MyRegistry(pyreg.Registry):
        pass

    yield MyRegistry("my_registry")


@pytest.fixture
def MyRegistered(my_registry: pyreg.Registry):
    class MyRegisteredInner(pyreg.Registered):
        class Config(pyreg.PyregConfig):
            registry = my_registry

    yield MyRegisteredInner
