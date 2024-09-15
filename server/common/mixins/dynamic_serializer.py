
class DynamicFieldsMixin:
    def __init__(self, *args, **kwargs):
        """  
        Mixin for Dynamic Field Management
        """
        fields = kwargs.pop('fields', None)
        exclude_fields = kwargs.pop('exclude_fields', None)
        read_only_fields = kwargs.pop('read_only_fields', None)
        write_only_fields = kwargs.pop('write_only_fields', None)
        super().__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)

        if exclude_fields is not None:
            for field_name in set(exclude_fields):
                self.fields.pop(field_name)

        if read_only_fields is not None:
            for field_name in set(read_only_fields):
                if field_name in self.fields:
                    self.fields[field_name].read_only = True

        if write_only_fields is not None:
            for field_name in set(write_only_fields):
                if field_name in self.fields:
                    self.fields[field_name].write_only = True
