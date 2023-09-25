import pyreg


def test_register_new_instance():
    class MyRegistry(pyreg.Registry):
        pass

    my_registry = MyRegistry("my_registry")

    class MyRegistered(pyreg.Registered):
        class Config(pyreg.PyregConfig):
            registry = my_registry

    MyRegistered()
    assert len(my_registry) == 1

    MyRegistered()
    assert len(my_registry) == 2


def test_register_same_instance_twice():
    class MyRegistry(pyreg.Registry):
        pass

    my_registry = MyRegistry("my_registry")

    class MyRegistered(pyreg.Registered):
        class Config(pyreg.PyregConfig):
            registry = my_registry

    same_instance = MyRegistered()
    assert len(my_registry) == 1

    my_registry.register(same_instance)
    assert len(my_registry) == 1
