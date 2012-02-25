=============
admin-sortable
=============

What is it?
=============
The adminsortable app adds generic drag-and-drop facilities
to any Django model class or Tabular Inline via Django Admin
and jQueryUI.

Installation
=============
1. Run ``setup.py`` or add ``adminsortable`` to your PYTHONPATH.
2. Copy the ``adminsortable`` folder from the static folder to the
location you server static files from, or if you're using the StaticFiles app
 https://docs.djangoproject.com/en/1.3/ref/contrib/staticfiles/,
run: $ python manage.py collectstatic to move the files to the location
you've specified for static files.
3. Add ``adminsortable`` to your INSTALLED_APPS.
4. Have a look at the included sample_project to see working examples.
The login credentials for admin are: admin/admin

When a model is sortable, a tool-area link will be added that says "Change Order".
Click this link, and you will be taken to the custom view where you can drag-and-drop
the records into order.

Tabular inlines may be drag-and-dropped into any order directly from the change form.

Usage
=============
Models
----------------------
To add sorting to a model, your model needs to inherit from ``Sortable`` and
have an inner Meta class that inherits from ``Sortable.Meta``

    #models.py
    from adminsortable.models import Sortable
    
    class MySortableClass(Sortable):
        class Meta(Sortable.Meta)
        
        title = models.CharField(max_length=50)
        
        def __unicode__(self):
            return self.title


It is also possible to order objects relative to another object that is a ForeignKey:

    from adminsortable.fields import SortableForeignKey

    #models.py
    class Category(models.Model):
        title = models.CharField(max_length=50)
        ...
    
    class Project(Sortable):
        class Meta(Sortable.Meta)
        
        category = SortableForeignKey(Category)
        title = models.CharField(max_length=50)
        
        def __unicode__(self):
            return self.title


Sortable has one field: `order` and adds a default ordering value set to `order`.

South
------
If you're adding Sorting to an existing model, it is recommended that you use django-south,
http://south.areacode.com/ to create a migration to add the "order" field to your model.


*Django Admin Usage*
To enable sorting in the admin, you need to inherit from SortableAdmin:

    from django.contrib import admin
    from myapp.models import MySortableClass
    from adminsortable.admin import SortableAdmin
    
    class MySortableAdminClass(SortableAdmin):
        """Any admin options you need go here"""
    
    admin.site.register(MySortableClass, MySortableAdminClass)


To enable sorting on TabularInline models, you need to inherit from
SortableTabularInline:

    from adminsortable.admin import SortableTabularInline
    
    class MySortableTabularInline(SortableTabularInline):
       """Your inline options go here"""


To enable sorting on StackedInline models, you need to inherit from
SortableStackedInline:

    from adminsortable.admin import SortableStackedInline
    
    class MySortableStackedInline(SortableStackedInline):
       """Your inline options go here"""

!!! *IMPORTANT* !!!
With stacked inline models, their height can dynamically increase,
which can cause sortable stacked inlines to not behave as expected.
If the height of the stacked inline is going to be very tall, I would
suggest NOT using SortableStackedInline. I'm currently working on
a way to make this more usable.


Rationale
=============
Other projects have added drag-and-drop ordering to the ChangeList
view, however this introduces a couple of problems...

- The ChangeList view supports pagination, which makes drag-and-drop
ordering across pages impossible.
- The ChangeList view by default, does not order records based on a
foreign key, nor distinguish between rows that are associated with a
foreign key. This makes ordering the records grouped by a foreign key
impossible.
- The ChangeList supports in-line editing, and adding drag-and-drop
ordering on top of that just seemed a little much in my opinion.

Status
=============
admin-sortable is currently used in production.


What's new in 1.3
=============
- Refactored ``sortable_by`` to subclass ForeignKey rather than a property or classmethod.
  No more extra property hackishness.

Features
=============
Current
---------
- Supports Django 1.3+
- Adds an admin view to any model that inherits from Sortable and SortableAdmin
that allows you to drag and drop objects into any order via jQueryUI.
- Adds drag and drop ordering to Tabular and Stacked Inline models that inherit from
SortableTabularInline and SortableStackedInline
- Allows ordering of objects that are sorted on a Foreign Key, and adds ordering
to the foreign key object if it also inherits from Sortable.
- Supports non-integer primary keys.

Future
------
- Support for foreign keys that are self referential
- More unit tests

Requirements
=============
Sample Project
----------------
Requires django-appmedia, included

License
=============
The admin-sortable app is released 
under the Apache Public License v2.
