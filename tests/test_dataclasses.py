import dataclasses

import pytest

import simpleregistry


@pytest.fixture
def MyDataclass(my_registry: simpleregistry.Registry):
    raise NotImplementedError


def test_works_with_frozen_eq_dataclass(my_registry: simpleregistry.Registry):
    @my_registry
    @dataclasses.dataclass(frozen=True, eq=True)
    class MyDataclass:
        str_field: str
        int_field: int

    my_dataclass = MyDataclass(str_field="a", int_field=1)

    assert my_dataclass in my_registry
    assert my_registry.all() == {my_dataclass}
    assert my_registry.filter(str_field="a") == {my_dataclass}
    assert my_registry.filter(int_field=0) == set()


def test_works_with_frozen_but_not_eq_dataclass(my_registry: simpleregistry.Registry):
    @my_registry
    @dataclasses.dataclass(frozen=True, eq=False)
    class MyDataclass:
        str_field: str
        int_field: int

    my_dataclass = MyDataclass(str_field="a", int_field=1)

    assert my_dataclass in my_registry
    assert my_registry.all() == {my_dataclass}
    assert my_registry.filter(str_field="a") == {my_dataclass}
    assert my_registry.filter(int_field=0) == set()


def test_works_with_unsafe_hash(my_registry: simpleregistry.Registry):
    @my_registry
    @dataclasses.dataclass(unsafe_hash=True)
    class MyDataclass:
        str_field: str
        int_field: int

    my_dataclass = MyDataclass(str_field="a", int_field=1)

    assert my_dataclass in my_registry
    assert my_registry.all() == {my_dataclass}
    assert my_registry.filter(str_field="a") == {my_dataclass}
    assert my_registry.filter(int_field=0) == set()


def test_works_with_custom_hash(my_registry: simpleregistry.Registry):
    @my_registry
    @dataclasses.dataclass
    class MyDataclass:
        str_field: str
        int_field: int

        def __hash__(self) -> int:
            return hash(f"{self.str_field}:{self.int_field}")

    my_dataclass = MyDataclass(str_field="a", int_field=1)

    assert my_dataclass in my_registry
    assert my_registry.all() == {my_dataclass}
    assert my_registry.filter(str_field="a") == {my_dataclass}
    assert my_registry.filter(int_field=0) == set()


def test_does_not_work_with_non_hashable(my_registry: simpleregistry.Registry):
    @my_registry
    @dataclasses.dataclass
    class MyDataclass:
        str_field: str
        int_field: int

    with pytest.raises(TypeError):
        MyDataclass(str_field="a", int_field=1)
