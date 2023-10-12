import pydantic.v1 as pydantic_v1
import pydantic as pydantic_v2

import simpleregistry


def test_works_with_pydantic_v1_frozen(my_registry: simpleregistry.Registry):
    @simpleregistry.register(my_registry)
    class MyPydanticModel(pydantic_v1.BaseModel):
        str_field: str
        int_field: int

        class Config:
            frozen = True

    my_pydantic_model = MyPydanticModel(str_field="a", int_field=1)

    assert my_pydantic_model in my_registry
    assert my_registry.all() == {my_pydantic_model}
    assert my_registry.filter(str_field="a") == {my_pydantic_model}
    assert my_registry.filter(int_field=0) == set()


def test_works_with_pydantic_v1_custom_hash(my_registry: simpleregistry.Registry):
    @simpleregistry.register(my_registry)
    class MyPydanticModel(pydantic_v1.BaseModel):
        str_field: str
        int_field: int

        def __hash__(self):
            return hash(f"{self.str_field}:{self.int_field}")

    my_pydantic_model = MyPydanticModel(str_field="a", int_field=1)

    assert my_pydantic_model in my_registry
    assert my_registry.all() == {my_pydantic_model}
    assert my_registry.filter(str_field="a") == {my_pydantic_model}
    assert my_registry.filter(int_field=0) == set()


def test_works_with_pydantic_v2_frozen(my_registry: simpleregistry.Registry):
    @simpleregistry.register(my_registry)
    class MyPydanticModel(pydantic_v2.BaseModel):
        str_field: str
        int_field: int

        class Config:
            frozen = True

    my_pydantic_model = MyPydanticModel(str_field="a", int_field=1)

    assert my_pydantic_model in my_registry
    assert my_registry.all() == {my_pydantic_model}
    assert my_registry.filter(str_field="a") == {my_pydantic_model}
    assert my_registry.filter(int_field=0) == set()


def test_works_with_pydantic_v2_custom_hash(my_registry: simpleregistry.Registry):
    @simpleregistry.register(my_registry)
    class MyPydanticModel(pydantic_v2.BaseModel):
        str_field: str
        int_field: int

        def __hash__(self):
            return hash(f"{self.str_field}:{self.int_field}")

    my_pydantic_model = MyPydanticModel(str_field="a", int_field=1)

    assert my_pydantic_model in my_registry
    assert my_registry.all() == {my_pydantic_model}
    assert my_registry.filter(str_field="a") == {my_pydantic_model}
    assert my_registry.filter(int_field=0) == set()
