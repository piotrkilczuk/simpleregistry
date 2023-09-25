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


def test_register_new_instance():
    class MyRegistry(pyreg.Registry):
        pass

    my_registry = MyRegistry("my_registry")

    class MyRegistered(pyreg.Registered):
        class Config(pyreg.PyregConfig):
            registry = my_registry

    MyRegistered()
    assert len(my_registry) == 1

    MyRegistered()
    assert len(my_registry) == 2


def test_register_same_instance_twice():
    class MyRegistry(pyreg.Registry):
        pass

    my_registry = MyRegistry("my_registry")

    class MyRegistered(pyreg.Registered):
        class Config(pyreg.PyregConfig):
            registry = my_registry

    same_instance = MyRegistered()
    assert len(my_registry) == 1

    my_registry.register(same_instance)
    assert len(my_registry) == 1
