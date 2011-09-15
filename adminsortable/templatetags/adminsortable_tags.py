from django import template

register = template.Library()


@register.inclusion_tag('adminsortable/shared/objects.html', takes_context=True)
def render_sortable_objects(context, objects):
    return {'objects' : objects}


@register.inclusion_tag('adminsortable/shared/nested_objects.html', takes_context=True)
def render_nested_sortable_objects(context, objects, group_expression):
    group_expression = context.get('group_expression')
    sortable_on_class = context.get('sortable_on_class')
    return {'objects' : objects, 'group_expression' : group_expression,
            'sortable_on_class' : sortable_on_class,
            'sortable_by_class_is_sortable' : context.get('sortable_by_class_is_sortable')}


@register.inclusion_tag('adminsortable/shared/list_items.html', takes_context=True)
def render_list_items(context, list_objects):
    return {'list_objects' : list_objects}


@register.inclusion_tag('adminsortable/shared/object_rep.html', takes_context=True)
def render_object_rep(context, object):
    return {'object' : object}
