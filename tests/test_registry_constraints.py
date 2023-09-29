import pytest

import simpleregistry


def test_polymorphism_allowed():
    polymorphic_registry = simpleregistry.Registry(
        "polymorphic_registry", allow_polymorphism=True
    )

    @polymorphic_registry
    class TypeOne:
        pass

    @polymorphic_registry
    class TypeTwo:
        pass

    one = TypeOne()
    two = TypeTwo()

    assert polymorphic_registry.all() == {one, two}


def test_polymorphism_not_allowed():
    non_polymorphic_registry = simpleregistry.Registry(
        "non_polymorphic_registry", allow_polymorphism=False
    )

    @non_polymorphic_registry
    class TypeOne:
        pass

    with pytest.raises(simpleregistry.exceptions.PolymorphismNotAllowed) as exc_info:

        @non_polymorphic_registry
        class TypeTwo:
            pass

    assert (
        exc_info.value.args[0]
        == "Can't register another type TypeTwo. Already registered: TypeOne"
    )


def test_subclasses_allowed_even_if_polymorphism_off():
    non_polymorphic_registry = simpleregistry.Registry(
        "non_polymorphic_registry", allow_polymorphism=False
    )

    @non_polymorphic_registry
    class TypeOne:
        pass

    class TypeTwo(TypeOne):
        pass

    one = TypeOne()
    two = TypeTwo()

    assert non_polymorphic_registry.all() == {one, two}


def test_unregistered_types_cannot_be_forced_into_registry():
    registry = simpleregistry.Registry("registry")

    @registry
    class TypeOne:
        pass

    class TypeTwo:
        pass

    one = TypeOne()
    two = TypeTwo()

    with pytest.raises(simpleregistry.exceptions.TypeNotAllowed) as exc_info:
        registry.register(two)


def test_check_type_off_unregistered_type_can_be_forced_into_registry():
    registry = simpleregistry.Registry("registry", check_type=False)

    @registry
    class TypeOne:
        pass

    class TypeTwo:
        pass

    one = TypeOne()
    two = TypeTwo()

    registry.register(two)

    assert registry.all() == {one, two}


def test_allow_subclasses_off_subclass_cannot_be_forced_into_registry():
    registry = simpleregistry.Registry("registry", allow_subclasses=False)

    @registry
    class TypeOne:
        pass

    class TypeTwo(TypeOne):
        pass

    one = TypeOne()
    two = TypeTwo()

    assert registry.all() == {one}
