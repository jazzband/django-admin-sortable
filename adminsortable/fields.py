from django.db.models.fields.related import ForeignKey


class SortableForeignKey(ForeignKey):
    """
    Field simply acts as a flag to determine the class to sort by.
    This field replaces previous functionality where `sortable_by` was
    defined as a model property that specified another model class.
    """

    def south_field_triple(self):
        try:
            from south.modelsinspector import introspector
            cls_name = '{0}.{1}'.format(
                self.__class__.__module__,
                self.__class__.__name__)
            args, kwargs = introspector(self)
            return cls_name, args, kwargs
        except ImportError:
            pass
