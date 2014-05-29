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
    `is_sortable` determines whether or not the Model is sortable by
    determining if the last value of `order` is greater than the default
    of 1, which should be present if there is only one object.

    `model_type_id` returns the ContentType.id for the Model that
    inherits Sortable

    `save` the override of save increments the last/highest value of
    order by 1
    """

    order = models.PositiveIntegerField(editable=False, default=1,
        db_index=True)
    is_sortable = False
    sorting_filters = ()

    # legacy support
    sortable_by = None

    class Meta:
        abstract = True
        ordering = ['order']

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
            raise MultipleSortableForeignKeyException(
                u'{0} may only have one SortableForeignKey'.format(self))

    def save(self, *args, **kwargs):
        if not self.id:
            try:
                self.order = self.__class__.objects.aggregate(
                    models.Max('order'))['order__max'] + 1
            except (TypeError, IndexError):
                pass

        super(Sortable, self).save(*args, **kwargs)
