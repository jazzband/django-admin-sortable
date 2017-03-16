from django.db.models.fields.related import ForeignKey


class SortableForeignKey(ForeignKey):
    """
    Field simply acts as a flag to determine the class to sort by.
    This field replaces previous functionality where `sortable_by` was
    defined as a model property that specified another model class.
    """
    pass
