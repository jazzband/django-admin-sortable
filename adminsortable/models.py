from django.contrib.contenttypes.models import ContentType
from django.db import models


class Sortable(models.Model):
    """
    Unfortunately, Django doesn't support using more than one AutoField in a model
    or this class could be simplified.

    `is_sortable` determines whether or not the Model is sortable by determining
    if the last value of `order` is greater than the default of 1, which should be
    present if there is only one object.

    `model_type_id` returns the ContentType.id for the Model that inherits Sortable

    `save` the override of save increments the last/highest value of order by 1
    """
    order = models.PositiveIntegerField(editable=False, default=1, db_index=True)

    class Meta:
        abstract = True
        ordering = ['order']

    @classmethod
    def is_sortable(cls):
        try:
            return True if cls.objects.order_by('-order')[:1][0].order > 1 else False
        except IndexError:
            return False

    @classmethod
    def model_type_id(cls):
        return ContentType.objects.get_for_model(cls).id

    def save(self, *args, **kwargs):
        if not self.id:
            try:
                #increment the order field by adding one to the last value of order
                self.order = self.__class__.objects.order_by('-order')[:1][0].order + 1
            except IndexError:
                #order defaults to 1
                pass
        super(Sortable, self).save(*args, **kwargs)
