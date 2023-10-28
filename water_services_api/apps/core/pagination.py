from django.core.paginator import InvalidPage
from django.http import HttpResponseNotFound
from rest_framework import pagination
from rest_framework.response import Response


class StandardLimonSetPagination(pagination.PageNumberPagination):
    page_size_query_param = 'per_page'
    page_query_param = 'current_page'

    def paginate_queryset(self, queryset, request, view=None):
        per_page = self.get_page_size(request)

        if not per_page:
            return None

        paginator = self.django_paginator_class(queryset, per_page)

        page_number = request.query_params.get(self.page_query_param, 1)
        if page_number in self.last_page_strings:
            page_number = paginator.num_pages

        try:
            if int(paginator.num_pages) < int(page_number):
                page_number = paginator.num_pages
            self.page = paginator.page(page_number)
        except InvalidPage as exc:
            msg = self.invalid_page_message.format(
                page_number=page_number, message="six.text_type(exc)"
            )
            return HttpResponseNotFound(msg)

        if paginator.num_pages > 1 and self.template is not None:
            self.display_page_controls = True

        self.request = request
        return list(self.page)

    def get_paginated_response(self, data):
        return Response({
            'pagination': {
                'current_page': self.page.number,
                'total': self.page.paginator.count,
                'from': self.page.start_index(),
                'to': self.page.end_index(),
                'per_page': self.page_size,
                'last_page': self.page.paginator.num_pages,
            },
            'status': True,
            'data': data,
        })


class CustomPagination():
    pagination_class = StandardLimonSetPagination
    page = StandardLimonSetPagination
