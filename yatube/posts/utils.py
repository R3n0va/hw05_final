from django.core.paginator import Paginator


PUB_NUMS = 10


def page_obj(request, queryset):
    paginator = Paginator(queryset, PUB_NUMS)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)
