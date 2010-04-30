import re

from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse
from django.template.loader import render_to_string

from content.filters import IntervalOrderFilterSet
from content.generic.views import GenericObjectDetail, GenericObjectList 
from gallery.models import Gallery, GalleryItem

def galleryimage_response(context):
    template = "gallery/ajax/galleriffic_galleryimage.html"
    return render_to_string(template, context)
    
def videoembed_response(context):
    template = "gallery/ajax/galleriffic_videoembed.html"
    result = render_to_string(template, context)
    result = re.sub('width=".{0,4}"', 'width="606"', result)
    result = re.sub('height=".{0,4}"', 'height="340"', result)
    return result
    
def videofile_response(context):
    template = "gallery/ajax/galleriffic_videofile.html"
    return render_to_string(template, context)

def gallery_item_ajax_galleriffic(request, slug):
    try:
        obj = GalleryItem.permitted.filter(slug=slug).get()
    except GalleryItem.DoesNotExist:
        raise Http404

    obj = obj.as_leaf_class()

    options = {
        'GalleryImage': galleryimage_response,
        'VideoEmbed': videoembed_response,
        'VideoFile': videofile_response,
    }
    
    context = {'object':  obj}
    result = options[obj._meta.object_name](context)
    return HttpResponse(result)

class ObjectList(GenericObjectList):
    def get_extra_context(self, *args, **kwargs):
        extra_context = super(ObjectList, self).get_extra_context(*args, **kwargs)
        added_context = {'title': 'Galleries'}
        if extra_context:
            extra_context.update(
                added_context,
            )
        else:
            extra_context = added_context

        return extra_context
    
    def get_filterset(self, request, queryset):
        return IntervalOrderFilterSet(request.GET, queryset=queryset)
    
    def get_paginate_by(self):
        return 12
    
    def get_queryset(self):
        return Gallery.permitted.all()

object_list = ObjectList()

class ObjectDetail(GenericObjectDetail):
    def get_queryset(self):
        return Gallery.permitted.all()
    
    def get_extra_context(self, *args, **kwargs):
        extra_context = super(ObjectDetail, self).get_extra_context(*args, **kwargs)
        added_context = {'title': 'Galleries'}
        if extra_context:
            extra_context.update(
                added_context,
            )
        else:
            extra_context = added_context

        return extra_context
    
    def get_filterset(self, request, queryset):
        return IntervalOrderFilterSet(request.GET, queryset=queryset, action_url=reverse('gallery_object_list'))

object_detail = ObjectDetail()
