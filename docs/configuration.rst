Configuring Django Admin Sortable
=================================

Configuring django-admin-sortable is quite simple:

    1. Add ``adminsortable`` to your ``INSTALLED_APPS``.
    2. Ensure ``django.core.context_processors.static`` is in your ``TEMPLATE_CONTEXT_PROCESSORS``.

Static Media
------------

django-admin-sortable includes a few CSS and JavaScript files. The preferred method of getting these files into your project is to use the `staticfiles app <https://docs.djangoproject.com/en/1.6/ref/contrib/staticfiles/>`_.

Alternatively, you can copy or symlink the ``adminsortable`` folder inside the ``static`` directory to the location you serve static files from.
