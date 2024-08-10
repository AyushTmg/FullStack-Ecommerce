from rest_framework.serializers import ModelSerializer


class DynamicModelSerializer(ModelSerializer):
    def __init__(self,instance=None,*args,**kwargs):
        """  
        Custom Serializer For Dynamic Usage
        """
        fields=kwargs.pop('fields',None)
        exclude_fields=kwargs.pop('exclude_fields',None)
        read_only_fields=kwargs.pop('read_only_fields',None)
        write_only_fields=kwargs.pop('write_only_fields',None)
        super().__init__(instance,*args,*kwargs)


        if fields is not None:
            required=set(fields)
            existing=set(self.fields.keys())
            for field_name in existing-required:
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

        

        
