from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings


def paginate(objects, page, items_per_page=settings.ENDLESS_PAGINATION_PER_PAGE):
    paginator = Paginator(objects, items_per_page)
    try:
        objects = paginator.page(page)
    except PageNotAnInteger:
        try:
            objects = paginator.page(1)
        except TypeError:
            objects = []
    except EmptyPage:
        objects = []
    return objects
