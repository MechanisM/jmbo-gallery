from django import template

register = template.Library()

@register.inclusion_tag('gallery/inclusion_tags/gallery_listing.html')
def gallery_listing(object_list):
    return {'object_list': object_list}

@register.inclusion_tag(
    'gallery/inclusion_tags/gallery_detail.html', 
    takes_context=True
)
def gallery_detail(context, obj):
    context['object'] = obj
    return context
