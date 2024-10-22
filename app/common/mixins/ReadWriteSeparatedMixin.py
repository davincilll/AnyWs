class ReadWriteSeparatedMixin:
    """
    对于custom_action使用何种序列化器由custom_action_use_write_serializer决定，默认为True
    """

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)

    read_serializer_class = None
    write_serializer_class = None
    custom_action_use_write_serializer = True

    def get_serializer_class(self):
        if self.custom_action_use_write_serializer:
            if self.action in ["list", "retrieve"]:
                return self.get_read_serializer_class()
            return self.get_write_serializer_class()
        if not self.custom_action_use_write_serializer:
            if self.action in ["create", "update", "partial_update", "destroy"]:
                return self.get_write_serializer_class()
            return self.get_read_serializer_class()

    def get_read_serializer_class(self):
        assert self.read_serializer_class is not None, (
                "'%s' should either include a `read_serializer_class` attribute,"
                "or override the `get_read_serializer_class()` method."
                % self.__class__.__name__
        )
        return self.read_serializer_class

    def get_write_serializer_class(self):
        assert self.write_serializer_class is not None, (
                "'%s' should either include a `write_serializer_class` attribute,"
                "or override the `get_write_serializer_class()` method."
                % self.__class__.__name__
        )
        return self.write_serializer_class
