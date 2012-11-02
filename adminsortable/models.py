from django.contrib.contenttypes.models import ContentType
from django.db import models

from adminsortable.fields import SortableForeignKey


class MultipleSortableForeignKeyException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class Sortable(models.Model):
    """
    Unfortunately, Django doesn't support using more than one AutoField in a model
    or this class could be simplified.

    `is_sortable` determines whether or not the Model is sortable by determining
    if the last value of `order` is greater than the default of 1, which should be
    present if there is only one object.

    `model_type_id` returns the ContentType.id for the Model that inherits Sortable

    `save` the override of save increments the last/highest value of order by 1

    Override `sortable_by` method to make your model be sortable by a foreign key field.
    Set `sortable_by` to the class specified in the foreign key relationship.
    """

    order = models.PositiveIntegerField(editable=False, default=1, db_index=True)

    # legacy support
    sortable_by = None

    class Meta:
        abstract = True
        ordering = ['order']

    @classmethod
    def is_sortable(cls):
        try:
            max_order = cls.objects.aggregate(models.Max('order'))['order__max']
        except (TypeError, IndexError):
            max_order = 0
        return True if max_order > 1 else False

    @classmethod
    def model_type_id(cls):
        return ContentType.objects.get_for_model(cls).id

    def __init__(self, *args, **kwargs):
        super(Sortable, self).__init__(*args, **kwargs)

        # Validate that model only contains at most one SortableForeignKey
        sortable_foreign_keys = []
        for field in self._meta.fields:
            if isinstance(field, SortableForeignKey):
                sortable_foreign_keys.append(field)
        if len(sortable_foreign_keys) > 1:
            raise MultipleSortableForeignKeyException(u'%s may only have one SortableForeignKey' % self)

    def save(self, *args, **kwargs):
        if not self.id:
            try:
                self.order = self.__class__.objects.aggregate(models.Max('order'))['order__max'] + 1
            except (TypeError, IndexError):
                pass

        super(Sortable, self).save(*args, **kwargs)
