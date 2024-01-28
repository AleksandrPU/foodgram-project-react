from rest_framework.pagination import PageNumberPagination

from foodgram_backend.constants import PAGINATION_PAGE_SIZE


class CustomPageNumberPagination(PageNumberPagination):
    page_size = PAGINATION_PAGE_SIZE
    page_size_query_param = 'limit'
