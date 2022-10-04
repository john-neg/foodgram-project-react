from rest_framework.pagination import PageNumberPagination


class CustomPageNumberPagination(PageNumberPagination):
    """
    Добавляет параметр 'limit', ограничивающий кол-во объектов на странице.
    """

    page_size_query_param = "limit"
