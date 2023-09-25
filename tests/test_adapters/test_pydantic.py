import pyreg
from pyreg import adapters


class MyRegistry(pyreg.Registry):
    pass


my_registry = MyRegistry("my_registry")


class MyRegistered(adapters.RegisteredModel):
    a_string_field: str
    a_numeric_field: int

    class Config(pyreg.PyregConfig):
        registry = my_registry
        hash_fields = ["a_string_field", "a_numeric_field"]


def test_can_instantiate_registered_model():
    assert MyRegistered(a_string_field="a", a_numeric_field=1)
    assert MyRegistered.Config.registry is my_registry
