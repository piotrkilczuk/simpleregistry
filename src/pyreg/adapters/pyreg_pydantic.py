import pydantic
from pydantic._internal import _model_construction

import pyreg


class RegisteredModelMeta(_model_construction.ModelMetaclass, pyreg.RegisteredMeta):
    @staticmethod
    def _validate_config(cls):
        super()._validate_config()
        if not hasattr(cls.Config, "hash_fields"):
            raise pyreg.PyregConfigurationError(
                f"Class {cls} doesn't have a Config.hash_fields"
            )
        if not isinstance(cls.Config.hash_fields, list):
            raise pyreg.PyregConfigurationError(
                f"Class {cls} has an invalid hash_fields: {cls.Config.hash_fields}"
            )


class RegisteredModel(
    pydantic.BaseModel, pyreg.Registered, metaclass=RegisteredModelMeta
):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Config.registry.register(self)

    def __hash__(self) -> int:
        hash_value = ":".join(
            [str(getattr(self, field)) for field in self.Config.hash_fields]
        )
        return hash(hash_value)
