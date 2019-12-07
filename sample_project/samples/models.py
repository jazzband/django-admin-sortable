import uuid

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from adminsortable.fields import SortableForeignKey
from adminsortable.models import Sortable, SortableMixin


class SimpleModel(models.Model):
    class Meta:
        abstract = True

    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title


# A model that is sortable
class Category(SimpleModel, SortableMixin):
    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['order']

    order = models.PositiveIntegerField(default=0, editable=False)


# A model with an override of its queryset for admin
class Widget(SimpleModel, SortableMixin):
    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title

    order = models.PositiveIntegerField(default=0, editable=False)


# A model that is sortable relative to a foreign key that is also sortable
# uses SortableForeignKey field. Works with versions 1.3+
class Project(SimpleModel, SortableMixin):
    class Meta:
        ordering = ['order']

    category = SortableForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField()
    isApproved = models.BooleanField(default=False)
    isFunded = models.BooleanField(default=False)

    order = models.PositiveIntegerField(default=0, editable=False)

    def get_next(self):
        return super(Project, self).get_next(
            filter_args=[models.Q(isApproved=True) | models.Q(isFunded=True)])


# Registered as a tabular inline on `Project`
class Credit(SortableMixin):
    class Meta:
        ordering = ['order']

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30, help_text="Given name")
    last_name = models.CharField(max_length=30, help_text="Family name")

    order = models.PositiveIntegerField(default=0, editable=False)

    def __str__(self):
        return '{0} {1}'.format(self.first_name, self.last_name)


# Registered as a stacked inline on `Project`
class Note(SortableMixin):
    class Meta:
        ordering = ['order']

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    text = models.CharField(max_length=100)

    order = models.PositiveIntegerField(default=0, editable=False)

    def __str__(self):
        return self.text


# Registered as a tabular inline on `Project` which can't be sorted
class NonSortableCredit(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30, help_text="Given name")
    last_name = models.CharField(max_length=30, help_text="Family name")

    def __str__(self):
        return '{0} {1}'.format(self.first_name, self.last_name)


# Registered as a stacked inline on `Project` which can't be sorted
class NonSortableNote(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    text = models.CharField(max_length=100)

    def __str__(self):
        return self.text


# A generic bound model
class GenericNote(SimpleModel, SortableMixin):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE,
        verbose_name=u"Content type", related_name="generic_notes")
    object_id = models.PositiveIntegerField(u"Content id")
    content_object = GenericForeignKey(ct_field='content_type',
        fk_field='object_id')

    order = models.PositiveIntegerField(default=0, editable=False)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return u'{0}: {1}'.format(self.title, self.content_object)


# An model registered as an inline that has a custom queryset
class Component(SimpleModel, SortableMixin):
    class Meta:
        ordering = ['order']

    widget = SortableForeignKey(Widget, on_delete=models.CASCADE)

    order = models.PositiveIntegerField(default=0, editable=False)

    def __str__(self):
        return self.title


class Person(SortableMixin):
    class Meta:
        ordering = ['order']
        verbose_name_plural = 'People'

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    is_board_member = models.BooleanField('Board Member', default=False)

    order = models.PositiveIntegerField(default=0, editable=False)

    # Sorting Filters allow you to set up sub-sets of objects that need
    # to have independent sorting. They are listed in order, from left
    # to right in the sorting change list. You can use any standard
    # Django ORM filter method.
    sorting_filters = (
        ('Board Members', {'is_board_member': True}),
        ('Non-Board Members', {'is_board_member': False}),
    )

    def __str__(self):
        return '{0} {1}'.format(self.first_name, self.last_name)


class NonSortableCategory(SimpleModel):
    class Meta(SimpleModel.Meta):
        verbose_name = 'Non-Sortable Category'
        verbose_name_plural = 'Non-Sortable Categories'

    def __str__(self):
        return self.title


class SortableCategoryWidget(SimpleModel, SortableMixin):
    class Meta:
        ordering = ['order']
        verbose_name = 'Sortable Category Widget'
        verbose_name_plural = 'Sortable Category Widgets'

    non_sortable_category = SortableForeignKey(
        NonSortableCategory, on_delete=models.CASCADE)

    order = models.PositiveIntegerField(default=0, editable=False)

    def __str__(self):
        return self.title


class SortableNonInlineCategory(SimpleModel, SortableMixin):
    """Example of a model that is sortable, but has a SortableForeignKey
    that is *not* sortable, and is also not defined as an inline of the
    SortableForeignKey field."""

    non_sortable_category = SortableForeignKey(
        NonSortableCategory, on_delete=models.CASCADE)

    order = models.PositiveIntegerField(default=0, editable=False)

    class Meta:
        ordering = ['order']
        verbose_name = 'Sortable Non-Inline Category'
        verbose_name_plural = 'Sortable Non-Inline Categories'

    def __str__(self):
        return self.title


class CustomWidget(SortableMixin, SimpleModel):

    # custom field for ordering
    custom_order_field = models.PositiveIntegerField(default=0, db_index=True,
        editable=False)

    class Meta:
        ordering = ['custom_order_field']
        verbose_name = 'Custom Widget'
        verbose_name_plural = 'Custom Widgets'

    def __str__(self):
        return self.title


class CustomWidgetComponent(SortableMixin, SimpleModel):

    custom_widget = models.ForeignKey(CustomWidget, on_delete=models.CASCADE)

    # custom field for ordering
    widget_order = models.PositiveIntegerField(default=0, db_index=True,
        editable=False)

    class Meta:
        ordering = ['widget_order']
        verbose_name = 'Custom Widget Component'
        verbose_name_plural = 'Custom Widget Components'

    def __str__(self):
        return self.title


class BackwardCompatibleWidget(Sortable, SimpleModel):

    class Meta(Sortable.Meta):
        verbose_name = 'Backward Compatible Widget'
        verbose_name_plural = 'Backward Compatible Widgets'

    def __str__(self):
        return self.title


class TestNonAutoFieldModel(SortableMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.PositiveIntegerField(editable=False, db_index=True)

    class Meta:
        ordering = ['order']
