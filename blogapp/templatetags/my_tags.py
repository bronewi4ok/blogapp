from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def param_replace(context, **kwargs):
    
    query = context['request'].GET.copy()
    for k, v in kwargs.items():
        query[k] = v
    for k in [k for k, v in query.items() if not v]:
        del query[k]
    return query.urlencode()

@register.filter
def get_name(value):
    spam = value.split('/')[-1]
    return spam