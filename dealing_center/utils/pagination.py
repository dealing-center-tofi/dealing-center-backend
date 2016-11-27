from rest_framework import pagination


class PageSizePagination(pagination.PageNumberPagination):
    page_size_query_param = 'page_size'


class AllObjectsPagination(PageSizePagination):
    def paginate_queryset(self, queryset, request, view=None):
        page_size = request.query_params.get(self.page_size_query_param)
        if page_size is not None and page_size == 'all':
            self.page_size = queryset.count() or 1
        return super(AllObjectsPagination, self).paginate_queryset(queryset, request, view)
