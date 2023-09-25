import pytest

import pyreg
from pyreg import exceptions


def test_registered_must_have_config_registry():
    class MyRegistry(pyreg.Registry):
        pass

    my_registry = MyRegistry("my_registry")

    class MyRegistered(pyreg.Registered):
        class Config(pyreg.PyregConfig):
            registry = my_registry

    assert MyRegistered()
    assert MyRegistered.Config.registry is my_registry


def test_registered_must_have_config_registry_but_does_not_have():
    with pytest.raises(exceptions.PyregConfigurationError):

        class MyRegistered(pyreg.Registered):
            pass


def test_registered_must_have_config_registry_but_registry_is_wrong_type():
    with pytest.raises(exceptions.PyregConfigurationError):

        class MyRegistered(pyreg.Registered):
            class Config:
                registry = {}
