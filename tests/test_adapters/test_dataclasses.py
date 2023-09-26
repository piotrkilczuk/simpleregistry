import dataclasses

import pytest

import pyreg
from pyreg.adapters import pyreg_dataclasses


class MyRegistry(pyreg.Registry):
    pass


my_registry = MyRegistry("my_registry")


def test_works_with_frozen_eq_dataclass():
    @dataclasses.dataclass(frozen=True, eq=True)
    class MyDataclass(pyreg_dataclasses.RegisteredDataclass):
        str_field: str
        int_field: int

        class Config(pyreg.PyregConfig):
            registry = my_registry

    my_dataclass = MyDataclass(str_field="a", int_field=1)

    assert my_dataclass in my_registry


def test_works_with_frozen_but_not_eq_dataclass():
    @dataclasses.dataclass(frozen=True, eq=False)
    class MyDataclass(pyreg_dataclasses.RegisteredDataclass):
        str_field: str
        int_field: int

        class Config(pyreg.PyregConfig):
            registry = my_registry

    my_dataclass = MyDataclass(str_field="a", int_field=1)

    assert my_dataclass in my_registry


def test_works_with_unsafe_hash():
    @dataclasses.dataclass(unsafe_hash=True)
    class MyDataclass(pyreg_dataclasses.RegisteredDataclass):
        str_field: str
        int_field: int

        class Config(pyreg.PyregConfig):
            registry = my_registry

    my_dataclass = MyDataclass(str_field="a", int_field=1)

    assert my_dataclass in my_registry


def test_works_with_custom_hash():
    @dataclasses.dataclass
    class MyDataclass(pyreg_dataclasses.RegisteredDataclass):
        str_field: str
        int_field: int

        def __hash__(self) -> int:
            return hash(f"{self.str_field}:{self.int_field}")

        class Config(pyreg.PyregConfig):
            registry = my_registry

    my_dataclass = MyDataclass(str_field="a", int_field=1)

    assert my_dataclass in my_registry


def test_does_not_work_with_non_hashable():
    @dataclasses.dataclass
    class MyDataclass(pyreg_dataclasses.RegisteredDataclass):
        str_field: str
        int_field: int

        class Config(pyreg.PyregConfig):
            registry = my_registry

    with pytest.raises(TypeError):
        MyDataclass(str_field="a", int_field=1)
