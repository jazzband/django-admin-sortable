Quickstart
==========

To get started using ``django-admin-sortable`` simply install it using ``pip``::

    $ pip install django-admin-sortable

Add ``adminsortable`` to your project's ``INSTALLED_APPS`` setting.

Ensure ``django.core.context_processors.static`` is in your ``TEMPLATE_CONTEXT_PROCESSORS`` setting.

Define your model, inheriting from ``adminsortable.Sortable``::

    # models.py
    from adminsortable.models import Sortable

    class MySortableClass(Sortable):
        class Meta(Sortable.Meta):
            pass

        title = models.CharField(max_length=50)

        def __unicode__(self):
            return self.title

Wire up your sortable model to Django admin::

    # admin.py
    from adminsortable.admin import SortableAdmin
    from .models import MySortableClass

    class MySortableAdminClass(SortableAdmin):
        """Any admin options you need go here"""

    admin.site.register(MySortableClass, MySortableAdminClass)

Your model's ChangeList view should now have an extra tool link when there are 2 or more objects present that will take you to a view where you can drag-and-drop the objects into your desired order.
