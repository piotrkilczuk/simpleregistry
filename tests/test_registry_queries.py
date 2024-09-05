import pytest

import simpleregistry
from simpleregistry import exceptions


@pytest.fixture()
def my_registry():
    class MyRegistry(simpleregistry.Registry):
        pass

    return MyRegistry("my_registry")


@pytest.fixture()
def MyRegistered(my_registry: simpleregistry.Registry):
    @my_registry
    class MyRegistered:
        str_field: str
        int_field: int

        def __init__(self, str_field: str, int_field: int):
            self.str_field = str_field
            self.int_field = int_field
            super().__init__()

    return MyRegistered


def test_all_empty(my_registry: simpleregistry.Registry):
    assert len(my_registry) == 0
    assert my_registry.all() == set()


def test_all_non_empty(my_registry: simpleregistry.Registry, MyRegistered):
    first_instance = MyRegistered("a", 1)
    second_instance = MyRegistered("b", 2)

    assert len(my_registry) == 2
    assert my_registry.all() == {first_instance, second_instance}


def test_filter_all_match(my_registry: simpleregistry.Registry, MyRegistered):
    first_instance = MyRegistered("a", 1)
    second_instance = MyRegistered("a", 2)

    assert len(my_registry) == 2
    assert my_registry.filter(str_field="a") == {first_instance, second_instance}


def test_filter_none_match(my_registry: simpleregistry.Registry, MyRegistered):
    MyRegistered("a", 1)
    MyRegistered("a", 2)

    assert len(my_registry) == 2
    assert my_registry.filter(str_field="b") == set()


def test_filter_some_match(my_registry: simpleregistry.Registry, MyRegistered):
    first_instance = MyRegistered("a", 1)
    MyRegistered("a", 2)

    assert len(my_registry) == 2
    assert my_registry.filter(str_field="a", int_field=1) == {first_instance}


def test_exclude_all_match(my_registry: simpleregistry.Registry, MyRegistered):
    MyRegistered("a", 1)
    MyRegistered("a", 2)

    assert len(my_registry) == 2
    assert my_registry.exclude(str_field="a") == set()


def test_exclude_some_match(my_registry: simpleregistry.Registry, MyRegistered):
    MyRegistered("a", 1)
    second_instance = MyRegistered("a", 2)

    assert len(my_registry) == 2
    assert my_registry.exclude(str_field="a", int_field=1) == {second_instance}


def test_exclude_none_match(my_registry: simpleregistry.Registry, MyRegistered):
    first_instance = MyRegistered("a", 1)
    second_instance = MyRegistered("a", 2)

    assert len(my_registry) == 2
    assert my_registry.exclude(str_field="a", int_field=3) == {
        first_instance,
        second_instance,
    }


def test_get_exactly_one_match(my_registry: simpleregistry.Registry, MyRegistered):
    first_instance = MyRegistered("a", 1)
    MyRegistered("a", 2)

    assert my_registry.get(str_field="a", int_field=1) == first_instance


def test_get_none_matches(my_registry: simpleregistry.Registry, MyRegistered):
    MyRegistered("a", 1)

    with pytest.raises(exceptions.NoMatch):
        assert my_registry.get(str_field="b")


def test_get_more_than_one_matches(my_registry: simpleregistry.Registry, MyRegistered):
    MyRegistered("a", 1)
    MyRegistered("a", 2)

    with pytest.raises(exceptions.MultipleMatches):
        my_registry.get(str_field="a")
