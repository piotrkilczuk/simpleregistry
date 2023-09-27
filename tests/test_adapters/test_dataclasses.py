import dataclasses

import pytest

import simpleregistry
from simpleregistry.adapters import pyreg_dataclasses


class MyRegistry(simpleregistry.Registry):
    pass


my_registry = MyRegistry("my_registry")


def test_works_with_frozen_eq_dataclass():
    my_registry.clear()

    @dataclasses.dataclass(frozen=True, eq=True)
    class MyDataclass(pyreg_dataclasses.RegisteredDataclass):
        str_field: str
        int_field: int

        class Config(simpleregistry.PyregConfig):
            registry = my_registry

    my_dataclass = MyDataclass(str_field="a", int_field=1)

    assert my_dataclass in my_registry
    assert my_registry.all() == {my_dataclass}
    assert my_registry.filter(str_field="a") == {my_dataclass}
    assert my_registry.filter(int_field=0) == set()


def test_works_with_frozen_but_not_eq_dataclass():
    my_registry.clear()

    @dataclasses.dataclass(frozen=True, eq=False)
    class MyDataclass(pyreg_dataclasses.RegisteredDataclass):
        str_field: str
        int_field: int

        class Config(simpleregistry.PyregConfig):
            registry = my_registry

    my_dataclass = MyDataclass(str_field="a", int_field=1)

    assert my_dataclass in my_registry
    assert my_registry.all() == {my_dataclass}
    assert my_registry.filter(str_field="a") == {my_dataclass}
    assert my_registry.filter(int_field=0) == set()


def test_works_with_unsafe_hash():
    my_registry.clear()

    @dataclasses.dataclass(unsafe_hash=True)
    class MyDataclass(pyreg_dataclasses.RegisteredDataclass):
        str_field: str
        int_field: int

        class Config(simpleregistry.PyregConfig):
            registry = my_registry

    my_dataclass = MyDataclass(str_field="a", int_field=1)

    assert my_dataclass in my_registry
    assert my_registry.all() == {my_dataclass}
    assert my_registry.filter(str_field="a") == {my_dataclass}
    assert my_registry.filter(int_field=0) == set()


def test_works_with_custom_hash():
    my_registry.clear()

    @dataclasses.dataclass
    class MyDataclass(pyreg_dataclasses.RegisteredDataclass):
        str_field: str
        int_field: int

        def __hash__(self) -> int:
            return hash(f"{self.str_field}:{self.int_field}")

        class Config(simpleregistry.PyregConfig):
            registry = my_registry

    my_dataclass = MyDataclass(str_field="a", int_field=1)

    assert my_dataclass in my_registry
    assert my_registry.all() == {my_dataclass}
    assert my_registry.filter(str_field="a") == {my_dataclass}
    assert my_registry.filter(int_field=0) == set()


def test_does_not_work_with_non_hashable():
    my_registry.clear()

    @dataclasses.dataclass
    class MyDataclass(pyreg_dataclasses.RegisteredDataclass):
        str_field: str
        int_field: int

        class Config(simpleregistry.PyregConfig):
            registry = my_registry

    with pytest.raises(TypeError):
        MyDataclass(str_field="a", int_field=1)
