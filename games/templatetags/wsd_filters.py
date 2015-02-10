from django import template
from django.template.defaultfilters import stringfilter
register = template.Library()


@register.filter
def add_class_to_field(field, css):
    return field.as_widget(attrs={"class": css})

@register.filter
@stringfilter
def title_prefix(value):
    return " - " + value if value else ""