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

    sortable_foreign_key = None

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

        sortable_foreign_keys_length = len(sortable_foreign_keys)
        if sortable_foreign_keys_length > 1:
            raise MultipleSortableForeignKeyException(
                u'{0} may only have one SortableForeignKey'.format(self))
        elif sortable_foreign_keys_length == 1:
            self.__class__.sortable_foreign_key = sortable_foreign_keys[0]

    def save(self, *args, **kwargs):
        if not self.id:
            try:
                self.order = self.__class__.objects.aggregate(
                    models.Max('order'))['order__max'] + 1
            except (TypeError, IndexError):
                pass

        super(Sortable, self).save(*args, **kwargs)

    def _filter_objects(self, filters, extra_filters, filter_on_sortable_fk):
        if extra_filters:
            filters.update(extra_filters)

        if self.sortable_foreign_key and filter_on_sortable_fk:
            # sfk_obj == sortable foreign key instance
            sfk_obj = getattr(self, self.sortable_foreign_key.name)
            filters.update(
                {self.sortable_foreign_key.name: sfk_obj.id})

        try:
            obj = self.__class__.objects.filter(**filters)[:1][0]
        except IndexError:
            obj = None

        return obj

    def get_next(self, extra_filters={}, filter_on_sortable_fk=True):
        return self._filter_objects({'order__gt': self.order},
            extra_filters, filter_on_sortable_fk)

    def get_previous(self, extra_filters={}, filter_on_sortable_fk=True):
        return self._filter_objects({'order__lt': self.order},
            extra_filters, filter_on_sortable_fk)
