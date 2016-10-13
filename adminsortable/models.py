from django import VERSION
from django.contrib.contenttypes.models import ContentType
from django.db import models

from adminsortable.fields import SortableForeignKey


class MultipleSortableForeignKeyException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class SortableMixin(models.Model):
    """
    `is_sortable` determines whether or not the Model is sortable by
    determining if the last value of the field used to determine the order
    of objects is greater than the default of 1, which should be present if
    there is only one object.

    `model_type_id` returns the ContentType.id for the Model that
    inherits Sortable

    `save` the override of save increments the last/highest value of
    `Meta.ordering` by 1
    """

    is_sortable = False
    sorting_filters = ()

    # legacy support
    sortable_by = None
    sortable_foreign_key = None

    class Meta:
        abstract = True

    @classmethod
    def model_type_id(cls):
        return ContentType.objects.get_for_model(cls).id

    def __init__(self, *args, **kwargs):
        super(SortableMixin, self).__init__(*args, **kwargs)

        # Check that Meta.ordering contains one value
        try:
            self.order_field_name = self._meta.ordering[0].replace('-', '')
        except IndexError:
            raise ValueError(u'You must define the Meta.ordering '
                u'property on your model.')

        # get the model field defined by `Meta.ordering`
        self.order_field = self._meta.get_field(self.order_field_name)

        integer_fields = (models.PositiveIntegerField, models.IntegerField,
            models.PositiveSmallIntegerField, models.SmallIntegerField,
            models.BigIntegerField,)

        # check that the order field is an integer type
        if not self.order_field or not isinstance(self.order_field,
                integer_fields):
            raise NotImplemented(u'You must define the field '
                '`Meta.ordering` refers to, and it must be of type: '
                'PositiveIntegerField, IntegerField, '
                'PositiveSmallIntegerField, SmallIntegerField, '
                'BigIntegerField')

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

    def _get_order_field_value(self):
        try:
            return int(self.order_field.value_to_string(self))
        except ValueError:
            raise u'The value from the specified order field could not be '
            'typecast to an integer.'

    def save(self, *args, **kwargs):
        needs_default = (self._state.adding if VERSION >= (1, 8) else not self.pk)
        if needs_default:
            try:
                current_max = self.__class__.objects.aggregate(
                    models.Max(self.order_field_name))[self.order_field_name + '__max'] or 0

                setattr(self, self.order_field_name, current_max + 1)
            except (TypeError, IndexError):
                pass

        super(SortableMixin, self).save(*args, **kwargs)

    def _filter_objects(self, filters, extra_filters, filter_on_sortable_fk):
        if extra_filters:
            filters.update(extra_filters)

        if self.sortable_foreign_key and filter_on_sortable_fk:
            # sfk_obj == sortable foreign key instance
            sfk_obj = getattr(self, self.sortable_foreign_key.name)
            filters.update(
                {self.sortable_foreign_key.name: sfk_obj.id})

        try:
            order_by = '-{0}'.format(self.order_field_name) \
                if '{0}__lt'.format(self.order_field_name) in filters.keys() \
                else self.order_field_name
            obj = self.__class__.objects.filter(
                **filters).order_by(order_by)[:1][0]
        except IndexError:
            obj = None

        return obj

    def get_next(self, extra_filters={}, filter_on_sortable_fk=True):
        return self._filter_objects(
            {'{0}__gt'.format(self.order_field_name): self._get_order_field_value()},
            extra_filters, filter_on_sortable_fk)

    def get_previous(self, extra_filters={}, filter_on_sortable_fk=True):
        return self._filter_objects(
            {'{0}__lt'.format(self.order_field_name): self._get_order_field_value()},
            extra_filters, filter_on_sortable_fk)


# for legacy support of existing implementations
class Sortable(SortableMixin):

    class Meta:
        abstract = True
        ordering = ['order']

    order = models.PositiveIntegerField(default=0, editable=False,
        db_index=True)
