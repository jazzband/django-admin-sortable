from django import template
from django.core.urlresolvers import reverse

register = template.Library()


@register.simple_tag(takes_context=True)
def render_sortable_objects(context, objects,
        sortable_objects_template='adminsortable/shared/objects.html'):
    context.update({'objects': objects})
    tmpl = template.loader.get_template(sortable_objects_template)
    return tmpl.render(context)


@register.simple_tag(takes_context=True)
def render_nested_sortable_objects(context, objects, group_expression,
        sortable_nested_objects_template='adminsortable/shared/nested_objects.html'):
    context.update({'objects': objects, 'group_expression': group_expression})
    tmpl = template.loader.get_template(sortable_nested_objects_template)
    return tmpl.render(context)


@register.simple_tag(takes_context=True)
def render_list_items(context, list_objects,
        sortable_list_items_template='adminsortable/shared/list_items.html'):
    context.update({'list_objects': list_objects})
    tmpl = template.loader.get_template(sortable_list_items_template)
    return tmpl.render(context)


@register.simple_tag(takes_context=True)
def render_object_rep(context, obj,
        sortable_object_rep_template='adminsortable/shared/object_rep.html'):
    context.update({'object': obj})
    tmpl = template.loader.get_template(sortable_object_rep_template)
    return tmpl.render(context)


@register.simple_tag(takes_context=False)
def get_do_sorting_url(obj):
    return reverse('admin:%s_do_sorting' % obj._meta.app_label,
        kwargs={'model_type_id': obj.model_type_id()})
