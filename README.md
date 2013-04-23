# Django Admin Sortable

This project makes it easy to add drag-and-drop ordering to any model in
Django admin. Inlines for a sortable model may also be made sortable,
enabling individual items or groups of items to be sortable.

## Requirements
jQuery


## Installation
1. pip install django-admin-sortable

--or--

Download django-admin-sortable from [source](https://github.com/iambrandontaylor/django-admin-sortable/archive/master.zip)

1. Unzip the directory and cd into the uncompressed project directory
2. *Optional: Enable your virtualenv
3. Run `$ python setup.py install` or add `adminsortable` to your PYTHONPATH.


## Configuration
1. Add `adminsortable` to your `INSTALLED_APPS`.
2. Ensure `django.core.context_processors.static` is in your `TEMPLATE_CONTEXT_PROCESSORS`.

### Static Media
Preferred:
Use the [staticfiles app](https://docs.djangoproject.com/en/1.4/ref/contrib/staticfiles/)

Alternate:
Copy the `adminsortable` folder from the `static` folder to the
location you server static files from.

### Testing
Have a look at the included sample_project to see working examples.
The login credentials for admin are: admin/admin

When a model is sortable, a tool-area link will be added that says "Change Order".
Click this link, and you will be taken to the custom view where you can drag-and-drop
the records into order.

Inlines may be drag-and-dropped into any order directly from the change form.


## Usage

### Models
To add sorting to a model, your model needs to inherit from `Sortable` and
have an inner Meta class that inherits from `Sortable.Meta`

    #models.py
    from adminsortable.models import Sortable

    class MySortableClass(Sortable):
        class Meta(Sortable.Meta):
            pass

        title = models.CharField(max_length=50)

        def __unicode__(self):
            return self.title


It is also possible to order objects relative to another object that is a ForeignKey,
even if that model does not inherit from Sortable:

    from adminsortable.fields import SortableForeignKey

    #models.py
    class Category(models.Model):
        title = models.CharField(max_length=50)
        ...

    class Project(Sortable):
        class Meta(Sortable.Meta):
            pass

        category = SortableForeignKey(Category)
        title = models.CharField(max_length=50)

        def __unicode__(self):
            return self.title


Sortable has one field: `order` and adds a default ordering value set to `order`.

### Adding Sortable to an existing model
If you're adding Sorting to an existing model, it is recommended that you use [django-south](http://south.areacode.com/) to create a schema migration to add the "order" field to your model. You will also need to create a data migration in order to add the appropriate values for the `order` column.

Example assuming a model named "Category":

    def forwards(self, orm):
        for index, category in enumerate(orm.Category.objects.all()):
            category.order = index + 1
            category.save()

See: [this link](http://south.readthedocs.org/en/latest/tutorial/part3.html) for more
information on Data Migrations.


### Django Admin
To enable sorting in the admin, you need to inherit from `SortableAdmin`:

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


There are also generic equivalents that you can inherit from:

    from adminsortable.admin import (SortableGenericTabularInline,
        SortableGenericStackedInline)
        """Your generic inline options go here"""


*** IMPORTANT  ***
With stacked inline models, their height can dynamically increase,
which can cause sortable stacked inlines to not behave as expected.
If the height of the stacked inline is going to be very tall, I would
suggest NOT using SortableStackedInline. I'm currently working on
a way to make this more usable.


### Rationale
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

### Status
django-admin-sortable is currently used in production.


### What's new in 1.4.2?
- Unicode support for the sort view title (thanks @knyazz)


### Future
- Support for foreign keys that are self referential
- More unit tests
- Move unit tests out of sample project
- Travis CI integration


### License
django-admin-sortable is released under the Apache Public License v2.
