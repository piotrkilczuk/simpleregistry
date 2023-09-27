import pytest

import simpleregistry
from simpleregistry import exceptions


def test_registered_must_have_config_registry():
    class MyRegistry(simpleregistry.Registry):
        pass

    my_registry = MyRegistry("my_registry")

    class MyRegistered(simpleregistry.Registered):
        class Config(simpleregistry.PyregConfig):
            registry = my_registry

    assert MyRegistered()
    assert MyRegistered.Config.registry is my_registry


def test_registered_must_have_config_registry_but_does_not_have():
    with pytest.raises(exceptions.PyregConfigurationError):

        class MyRegistered(simpleregistry.Registered):
            pass


def test_registered_must_have_config_registry_but_registry_is_wrong_type():
    with pytest.raises(exceptions.PyregConfigurationError):

        class MyRegistered(simpleregistry.Registered):
            class Config:
                registry = {}
