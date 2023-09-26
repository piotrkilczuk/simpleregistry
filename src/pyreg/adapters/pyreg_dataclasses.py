import pyreg


class RegisteredDataclass(metaclass=pyreg.RegisteredMeta):
    def __post_init__(self):
        self.Config.registry.register(self)
