from django import template
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

register = template.Library()


@register.inclusion_tag('pagination.html', takes_context=True)
def render_pagination(context, object_list, page_count=20):
    paginator = Paginator(object_list, page_count)
    page = context['request'].GET.get('page')

    try:
        objects = paginator.page(page)
    except PageNotAnInteger:
        objects = paginator.page(1)
    except EmptyPage:
        objects = paginator.page(paginator.num_pages)

    context['objects'] = objects
    return context

