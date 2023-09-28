import simpleregistry


def test_register_new_instance(my_registry: simpleregistry.Registry):
    @simpleregistry.register(my_registry)
    class MyRegistered:
        pass

    MyRegistered()
    assert len(my_registry) == 1

    MyRegistered()
    assert len(my_registry) == 2


def test_register_same_instance_twice(my_registry: simpleregistry.Registry):
    @simpleregistry.register(my_registry)
    class MyRegistered:
        pass

    same_instance = MyRegistered()
    assert len(my_registry) == 1

    my_registry.register(same_instance)
    assert len(my_registry) == 1
