from typing import Type

import pyreg


class OtherRegistry(pyreg.Registry):
    pass


other_registry = OtherRegistry("other_registry")


def test__contains__empty_registry(
    my_registry: pyreg.Registry, MyRegistered: Type[pyreg.Registered]
):
    my_registered = MyRegistered()
    assert my_registered not in other_registry


def test__contains__non_empty_registry(
    my_registry: pyreg.Registry, MyRegistered: Type[pyreg.Registered]
):
    my_registered = MyRegistered()
    assert my_registered in my_registry


def test__len__empty_registry(
    my_registry: pyreg.Registry, MyRegistered: Type[pyreg.Registered]
):
    assert len(my_registry) == 0


def test__len__non_empty_registry(
    my_registry: pyreg.Registry, MyRegistered: Type[pyreg.Registered]
):
    MyRegistered()
    assert len(my_registry) == 1
