import simpleregistry


def test_register_new_instance():
    class MyRegistry(simpleregistry.Registry):
        pass

    my_registry = MyRegistry("my_registry")

    class MyRegistered(simpleregistry.Registered):
        class Config(simpleregistry.PyregConfig):
            registry = my_registry

    MyRegistered()
    assert len(my_registry) == 1

    MyRegistered()
    assert len(my_registry) == 2


def test_register_same_instance_twice():
    class MyRegistry(simpleregistry.Registry):
        pass

    my_registry = MyRegistry("my_registry")

    class MyRegistered(simpleregistry.Registered):
        class Config(simpleregistry.PyregConfig):
            registry = my_registry

    same_instance = MyRegistered()
    assert len(my_registry) == 1

    my_registry.register(same_instance)
    assert len(my_registry) == 1


def test_register_via_decorator(my_registry: simpleregistry.Registry):
    @simpleregistry.register(registry=my_registry)
    class MyRegistered:
        pass

    MyRegistered()
    assert len(my_registry) == 1
