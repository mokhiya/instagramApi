from rest_framework import pagination
from rest_framework.response import Response


class PostsPagination(pagination.PageNumberPagination):
    page_size = 5
    max_page_size = 10
    page_query_param = 'page'
    page_size_query_param = 'size'


    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data,
        })
