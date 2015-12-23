from itertools import groupby

import django
from django import template
try:
    from django import TemplateSyntaxError
except ImportError:
    #support for django 1.3
    from django.template.base import TemplateSyntaxError

register = template.Library()


class DynamicRegroupNode(template.Node):
    """
    Extends Django's regroup tag to accept a variable instead of a string literal
    for the property you want to regroup on
    """

    def __init__(self, target, parser, expression, var_name):
        self.target = target
        self.expression = template.Variable(expression)
        self.var_name = var_name
        self.parser = parser

    def render(self, context):
        obj_list = self.target.resolve(context, True)
        if obj_list is None:
            # target variable wasn't found in context; fail silently.
            context[self.var_name] = []
            return ''
        # List of dictionaries in the format:
        # {'grouper': 'key', 'list': [list of contents]}.

        #Try to resolve the filter expression from the template context.
        #If the variable doesn't exist, accept the value that passed to the
        #template tag and convert it to a string
        try:
            exp = self.expression.resolve(context)
        except template.VariableDoesNotExist:
            exp = str(self.expression)

        filter_exp = self.parser.compile_filter(exp)

        context[self.var_name] = [
            {'grouper': key, 'list': list(val)}
            for key, val in
            groupby(obj_list, lambda v, f=filter_exp.resolve: f(v, True))
        ]

        return ''


@register.tag
def dynamic_regroup(parser, token):
    """
    Django expects the value of `expression` to be an attribute available on
    your objects. The value you pass to the template tag gets converted into a
    FilterExpression object from the literal.

    Sometimes we need the attribute to group on to be dynamic. So, instead
    of converting the value to a FilterExpression here, we're going to pass the
    value as-is and convert it in the Node.
    """
    firstbits = token.contents.split(None, 3)
    if len(firstbits) != 4:
        raise TemplateSyntaxError("'regroup' tag takes five arguments")
    target = parser.compile_filter(firstbits[1])
    if firstbits[2] != 'by':
        raise TemplateSyntaxError("second argument to 'regroup' tag must be 'by'")
    lastbits_reversed = firstbits[3][::-1].split(None, 2)
    if lastbits_reversed[1][::-1] != 'as':
        raise TemplateSyntaxError("next-to-last argument to 'regroup' tag must"
                                  " be 'as'")

    expression = lastbits_reversed[2][::-1]
    var_name = lastbits_reversed[0][::-1]
    #We also need to hand the parser to the node in order to convert the value
    #for `expression` to a FilterExpression.
    return DynamicRegroupNode(target, parser, expression, var_name)


@register.assignment_tag
def get_django_version():
    version = django.VERSION
    return {'major': version[0], 'minor': version[1]}
