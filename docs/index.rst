.. Django Admin Sortable documentation master file, created by
   sphinx-quickstart on Wed Aug 20 14:40:56 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Django Admin Sortable's documentation!
=================================================

Django Admin Sortable is a super-easy way to add drag-and-drop ordering to almost any model you manage through Django admin. Inlines for a sortable model may also be made sortable, enabling individual items or groups of items to be sortable.

Supported Django Versions
-------------------------

Django 1.4.x
^^^^^^^^^^^^

Use django-admin-sortable 1.4.9 or below.

.. note::

    v1.5.2 introduced backwards incompatible changes for Django 1.4.x

Django >= 1.5.x
^^^^^^^^^^^^^^^^^^^^^^^

Use the latest version of django-admin-sortable.

.. warning::

    v1.6.6 introduced a backwards-incompatible change for ``sorting_filters``. Please update your ``sorting_filters`` attribute(s) to the new, tuple-based format.

What's New in |version|?
------------------------

- Python 2.6 backwards compatibility. Thanks `@EnTeQuAk <https://github.com/EnTeQuAk>`_


Contents:
---------

.. toctree::
   :maxdepth: 3

   quickstart
   configuration
   usage
   django-cms
   known-issues
   testing
   rationale
   status
   future
   license

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

