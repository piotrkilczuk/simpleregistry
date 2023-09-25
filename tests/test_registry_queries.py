import dataclasses

import pyreg


class MyRegistry(pyreg.Registry):
    pass


my_registry = MyRegistry("my_registry")


class MyRegistered(pyreg.Registered):
    str_field: str
    int_field: int

    def __init__(self, str_field: str, int_field: int):
        self.str_field = str_field
        self.int_field = int_field
        super().__init__()

    class Config(pyreg.PyregConfig):
        registry = my_registry


def test_all_empty():
    my_registry.clear()
    assert len(my_registry) == 0
    assert my_registry.all() == set()


def test_all_non_empty():
    my_registry.clear()

    first_instance = MyRegistered("a", 1)
    second_instance = MyRegistered("b", 2)

    assert len(my_registry) == 2
    assert my_registry.all() == {first_instance, second_instance}


def test_filter_all_match():
    my_registry.clear()

    first_instance = MyRegistered("a", 1)
    second_instance = MyRegistered("a", 2)

    assert len(my_registry) == 2
    assert my_registry.filter(str_field="a") == {first_instance, second_instance}


def test_filter_none_match():
    my_registry.clear()

    MyRegistered("a", 1)
    MyRegistered("a", 2)

    assert len(my_registry) == 2
    assert my_registry.filter(str_field="b") == set()


def test_filter_some_match():
    my_registry.clear()

    first_instance = MyRegistered("a", 1)
    MyRegistered("a", 2)

    assert len(my_registry) == 2
    assert my_registry.filter(str_field="a", int_field=1) == {first_instance}
