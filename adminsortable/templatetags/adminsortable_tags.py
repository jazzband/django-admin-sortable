from django.template.loader import render_to_string

from django import template
register = template.Library()


@register.simple_tag(takes_context=True)
def render_sortable_objects(context, objects,
        sortable_objects_template='adminsortable/shared/objects.html'):
    context.update({'objects': objects})
    return render_to_string(sortable_objects_template, context.flatten())


@register.simple_tag(takes_context=True)
def render_nested_sortable_objects(context, objects, group_expression,
        sortable_nested_objects_template='adminsortable/shared/nested_objects.html'):
    context.update({'objects': objects, 'group_expression': group_expression})
    return render_to_string(sortable_nested_objects_template, context.flatten())


@register.simple_tag(takes_context=True)
def render_list_items(context, list_objects,
        sortable_list_items_template='adminsortable/shared/list_items.html'):
    context.update({'list_objects': list_objects})
    return render_to_string(sortable_list_items_template, context.flatten())


@register.simple_tag(takes_context=True)
def render_object_rep(context, obj, forloop,
        sortable_object_rep_template='adminsortable/shared/object_rep.html'):
    context.update({'object': obj, 'forloop': forloop})
    return render_to_string(sortable_object_rep_template, context.flatten())
