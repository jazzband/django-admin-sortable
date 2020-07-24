Using Django Admin Sortable
===========================

Models
------

To add sorting to a model, your model needs to inherit from ``SortableMixin`` and at minimum, define an inner ``Meta.ordering`` value

    .. code-block:: python

    # models.py
    from adminsortable.models import Sortable

    class MySortableClass(Sortable):
        class Meta(Sortable.Meta):
            pass

        title = models.CharField(max_length=50)

        def __unicode__(self):
            return self.title

It is also possible to order objects relative to another object that is a ForeignKey.

.. note:: A small caveat here is that ``Category`` must also either inherit from ``Sortable`` or include an ``order`` property which is a ``PositiveSmallInteger`` field. This is due to the way Django admin instantiates classes.

    .. code-block:: python

    # models.py
    from adminsortable.fields import SortableForeignKey

    class Category(Sortable):
        class Meta(Sortable.Meta):
            pass

        title = models.CharField(max_length=50)
        ...

    class Project(Sortable):
        class Meta(Sortable.Meta):
            pass

        category = SortableForeignKey(Category)
        title = models.CharField(max_length=50)

        def __unicode__(self):
            return self.title

``Sortable`` has one field: ``order`` and adds a default ordering value set to ``order``, ascending.

Adding Sortable to an existing model
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you're adding Sorting to an existing model, it is recommended that you use `django-south <http://south.areacode.com/>`_ to create a schema migration to add the "order" field to your model. You will also need to create a data migration in order to add the appropriate values for the ``order`` column.

Example assuming a model named "Category"::

    .. code-block:: python

    def forwards(self, orm):
        for index, category in enumerate(orm.Category.objects.all()):
            category.order = index + 1
            category.save()

See `this link <http://south.readthedocs.org/en/latest/tutorial/part3.html>`_ for more information on Data Migrations.

Django Admin
------------

To enable sorting in the admin, you need to inherit from ``SortableAdmin``::

    .. code-block:: python

        from django.contrib import admin
        from myapp.models import MySortableClass
        from adminsortable.admin import SortableAdmin

        class MySortableAdminClass(SortableAdmin):
            """Any admin options you need go here"""

        admin.site.register(MySortableClass, MySortableAdminClass)

To enable sorting on TabularInline models, you need to inherit from SortableTabularInline::

    .. code-block:: python

    from adminsortable.admin import SortableTabularInline

    class MySortableTabularInline(SortableTabularInline):
        """Your inline options go here"""

To enable sorting on StackedInline models, you need to inherit from SortableStackedInline::

    .. code-block:: python

    from adminsortable.admin import SortableStackedInline

    class MySortableStackedInline(SortableStackedInline):
        """Your inline options go here"""

There are also generic equivalents that you can inherit from::

    .. code-block:: python

    from adminsortable.admin import (SortableGenericTabularInline,
        SortableGenericStackedInline)
        """Your generic inline options go here"""

Overriding ``queryset()``
^^^^^^^^^^^^^^^^^^^^^^^^^

django-admin-sortable supports custom queryset overrides on admin models and inline models in Django admin!

If you're providing an override of a ``SortableAdmin`` or ``Sortable`` inline model, you don't need to do anything extra. django-admin-sortable will automatically honor your queryset.

Have a look at the ``WidgetAdmin`` class in the sample project for an example of an admin class with a custom ``queryset()`` override.

Overriding ``queryset()`` for an inline model
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This is a special case, which requires a few lines of extra code to properly determine the sortability of your model. Example::

    .. code-block:: python

    # add this import to your admin.py
    from adminsortable.utils import get_is_sortable


    class ComponentInline(SortableStackedInline):
        model = Component

        def queryset(self, request):
            qs = super(ComponentInline, self).queryset(request).filter(
                title__icontains='foo')

            # You'll need to add these lines to determine if your model
            # is sortable once we hit the change_form() for the parent model.

            if get_is_sortable(qs):
                self.model.is_sortable = True
            else:
                self.model.is_sortable = False
            return qs

If you override the queryset of an inline, the number of objects present may change, and adminsortable won't be able to automatically determine if the inline model is sortable from here, which is why we have to set the ``is_sortable`` property of the model in this method.

Sorting subsets of objects
^^^^^^^^^^^^^^^^^^^^^^^^^^

It is also possible to sort a subset of objects in your model by adding a ``sorting_filters`` tuple. This works exactly the same as ``.filter()`` on a QuerySet, and is applied *after* ``get_queryset()`` on the admin class, allowing you to override the queryset as you would normally in admin but apply additional filters for sorting. The text "Change Order of" will appear before each filter in the Change List template, and the filter groups are displayed from left to right in the order listed. If no ``sorting_filters`` are specified, the text "Change Order" will be displayed for the link.

An example of sorting subsets would be a "Board of Directors". In this use case, you have a list of "People" objects. Some of these people are on the Board of Directors and some not, and you need to sort them independently::

    .. code-block:: python

    class Person(Sortable):
        class Meta(Sortable.Meta):
            verbose_name_plural = 'People'

        first_name = models.CharField(max_length=50)
        last_name = models.CharField(max_length=50)
        is_board_member = models.BooleanField('Board Member', default=False)

        sorting_filters = (
            ('Board Members', {'is_board_member': True}),
            ('Non-Board Members', {'is_board_member': False}),
        )

        def __unicode__(self):
            return '{} {}'.format(self.first_name, self.last_name)


.. warning::

    django-admin-sortable 1.6.6 introduces a backwards-incompatible change for ``sorting_filters``. Previously this attribute was defined as a dictionary, so you'll need to change your values over to the new tuple-based format.

Extending custom templates
^^^^^^^^^^^^^^^^^^^^^^^^^^

By default, adminsortable's change form and change list views inherit from Django admin's standard templates. Sometimes you need to have a custom change form or change list, but also need adminsortable's CSS and JavaScript for inline models that are sortable for example.

``SortableAdmin`` has two attributes you can override for this use case::

    change_form_template_extends
    change_list_template_extends

These attributes have default values of::

    .. code-block:: python

    change_form_template_extends = 'admin/change_form.html'
    change_list_template_extends = 'admin/change_list.html'

If you need to extend the inline change form templates, you'll need to select the right one, depending on your version of Django. For Django 1.5.x or below, you'll need to extend one of the following::

    templates/adminsortable/edit_inline/stacked-1.5.x.html
    templates/adminsortable/edit_inline/tabular-inline-1.5.x.html

For Django >= 1.6.x, extend::

    templates/adminsortable/edit_inline/stacked.html
    templates/adminsortable/edit_inline/tabular.html

.. note::

    A Special Note About Stacked Inlines...
    The height of a stacked inline model can dynamically increase, which can make them difficult to sort. If you anticipate the height of a stacked inline is going to be very tall, I would suggest using TabularStackedInline instead.
