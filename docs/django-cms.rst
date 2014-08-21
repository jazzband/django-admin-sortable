Django-CMS Integration
======================

Django-CMS plugins use their own change form, and thus won't automatically include the necessary JavaScript for django-admin-sortable to work. Fortunately, this is easy to resolve, as the ``CMSPlugin`` class allows a change form template to be specified::

    # example plugin
    from cms.plugin_base import CMSPluginBase

    class CMSCarouselPlugin(CMSPluginBase):
        admin_preview = False
        change_form_template = 'cms/sortable-stacked-inline-change-form.html'
        inlines = [SlideInline]
        model = Carousel
        name = _('Carousel')
        render_template = 'carousels/carousel.html'

        def render(self, context, instance, placeholder):
            context.update({
                'carousel': instance,
                'placeholder': placeholder
            })
            return context

    plugin_pool.register_plugin(CMSCarouselPlugin)

The contents of sortable-stacked-inline-change-form.html at a minimum need to extend the extrahead block with::

    {% extends "admin/cms/page/plugin_change_form.html" %}
    {% load static from staticfiles %}

    {% block extrahead %}
        {{ block.super }}
        <script type="text/javascript" src="{% static 'adminsortable/js/jquery-ui-django-admin.min.js' %}"></script>
        <script type="text/javascript" src="{% static 'adminsortable/js/jquery.django-csrf.js' %}"></script>
        <script type="text/javascript" src="{% static 'adminsortable/js/admin.sortable.stacked.inlines.js' %}"></script>

        <link rel="stylesheet" type="text/css" href="{% static 'adminsortable/css/admin.sortable.inline.css' %}" />
    {% endblock extrahead %}

Sorting within Django-CMS is really only feasible for inline models of a plugin as Django-CMS already includes sorting for plugin instances. For tabular inlines, just substitute::

    <script type="text/javascript" src="{% static 'adminsortable/js/admin.sortable.stacked.inlines.js' %}"></script>

with::

    <script type="text/javascript" src="{% static 'adminsortable/js/admin.sortable.tabular.inlines.js' %}"></script>

