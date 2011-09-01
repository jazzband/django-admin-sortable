from django.contrib.contenttypes.models import ContentType
from django.db import models


class Sortable(models.Model):
    order = models.PositiveIntegerField(editable=False, default=1, db_index=True)

    class Meta:
        abstract = True
        ordering = ['order', 'id']

    @classmethod
    def is_sortable(cls):
        return True if cls.objects.count() > 1 else False

    @classmethod
    def model_type_id(cls):
        return ContentType.objects.get_for_model(cls).id

    def save(self, *args, **kwargs):
        if not self.id:
            self.order = self.__class__.objects.count() + 1
        super(Sortable, self).save(*args, **kwargs)
