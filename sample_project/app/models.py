from django import VERSION

if VERSION < (1, 9):
    from django.contrib.contenttypes.generic import GenericForeignKey
else:
    from django.contrib.contenttypes.fields import GenericForeignKey

from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from adminsortable.fields import SortableForeignKey
from adminsortable.models import Sortable, SortableMixin


@python_2_unicode_compatible
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

    order = models.PositiveIntegerField(default=0)


# A model with an override of its queryset for admin
@python_2_unicode_compatible
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

    category = SortableForeignKey(Category)
    description = models.TextField()

    order = models.PositiveIntegerField(default=0, editable=False)


# Registered as a tabular inline on `Project`
@python_2_unicode_compatible
class Credit(SortableMixin):
    class Meta:
        ordering = ['order']

    project = models.ForeignKey(Project)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    order = models.PositiveIntegerField(default=0, editable=False)

    def __str__(self):
        return '{0} {1}'.format(self.first_name, self.last_name)


# Registered as a stacked inline on `Project`
@python_2_unicode_compatible
class Note(SortableMixin):
    class Meta:
        ordering = ['order']

    project = models.ForeignKey(Project)
    text = models.CharField(max_length=100)

    order = models.PositiveIntegerField(default=0, editable=False)

    def __str__(self):
        return self.text


# Registered as a tabular inline on `Project` which can't be sorted
@python_2_unicode_compatible
class NonSortableCredit(models.Model):
    project = models.ForeignKey(Project)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    def __str__(self):
        return '{0} {1}'.format(self.first_name, self.last_name)


# Registered as a stacked inline on `Project` which can't be sorted
@python_2_unicode_compatible
class NonSortableNote(models.Model):
    project = models.ForeignKey(Project)
    text = models.CharField(max_length=100)

    def __str__(self):
        return self.text


# A generic bound model
@python_2_unicode_compatible
class GenericNote(SimpleModel, SortableMixin):
    content_type = models.ForeignKey(ContentType,
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
@python_2_unicode_compatible
class Component(SimpleModel, SortableMixin):
    class Meta:
        ordering = ['order']

    widget = SortableForeignKey(Widget)

    order = models.PositiveIntegerField(default=0, editable=False)

    def __str__(self):
        return self.title


@python_2_unicode_compatible
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


@python_2_unicode_compatible
class NonSortableCategory(SimpleModel):
    class Meta(SimpleModel.Meta):
        verbose_name = 'Non-Sortable Category'
        verbose_name_plural = 'Non-Sortable Categories'

    def __str__(self):
        return self.title


@python_2_unicode_compatible
class SortableCategoryWidget(SimpleModel, SortableMixin):
    class Meta:
        ordering = ['order']
        verbose_name = 'Sortable Category Widget'
        verbose_name_plural = 'Sortable Category Widgets'

    non_sortable_category = SortableForeignKey(NonSortableCategory)

    order = models.PositiveIntegerField(default=0, editable=False)

    def __str__(self):
        return self.title


@python_2_unicode_compatible
class SortableNonInlineCategory(SimpleModel, SortableMixin):
    """Example of a model that is sortable, but has a SortableForeignKey
    that is *not* sortable, and is also not defined as an inline of the
    SortableForeignKey field."""

    non_sortable_category = SortableForeignKey(NonSortableCategory)

    order = models.PositiveIntegerField(default=0, editable=False)

    class Meta:
        ordering = ['order']
        verbose_name = 'Sortable Non-Inline Category'
        verbose_name_plural = 'Sortable Non-Inline Categories'

    def __str__(self):
        return self.title


@python_2_unicode_compatible
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


@python_2_unicode_compatible
class CustomWidgetComponent(SortableMixin, SimpleModel):

    custom_widget = models.ForeignKey(CustomWidget)

    # custom field for ordering
    widget_order = models.PositiveIntegerField(default=0, db_index=True,
        editable=False)

    class Meta:
        ordering = ['widget_order']
        verbose_name = 'Custom Widget Component'
        verbose_name_plural = 'Custom Widget Components'

    def __str__(self):
        return self.title


@python_2_unicode_compatible
class BackwardCompatibleWidget(Sortable, SimpleModel):

    class Meta(Sortable.Meta):
        verbose_name = 'Backward Compatible Widget'
        verbose_name_plural = 'Backward Compatible Widgets'

    def __str__(self):
        return self.title
