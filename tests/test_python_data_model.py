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


def test__iter__empty_registry(
    my_registry: pyreg.Registry, MyRegistered: Type[pyreg.Registered]
):

    assert {m for m in my_registry} == set()
    assert {m for m in my_registry} == set()


def test__iter__empty_registry(
    my_registry: pyreg.Registry, MyRegistered: Type[pyreg.Registered]
):
    my_registered_first = MyRegistered()
    my_registered_second = MyRegistered()

    # This can fail as the set is unordered, adjust if it does
    assert {m for m in my_registry} == {my_registered_first, my_registered_second}
    assert {m for m in my_registry} == {my_registered_first, my_registered_second}
