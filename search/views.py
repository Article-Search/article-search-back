import abc

from django.http import HttpResponse
from django_elasticsearch_dsl_drf.constants import LOOKUP_QUERY_IN, LOOKUP_FILTER_RANGE
from elasticsearch_dsl import Q
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from articles.documents import ArticleDocument
from articles.serializers import ArticleDocumentSerializer
from articles.views import ArticleDocumentView


class PaginatedElasticSearchAPIView(APIView, LimitOffsetPagination):
    serializer_class = None
    document_class = None

    @abc.abstractmethod
    def generate_q_expression(self, query):
        """This method should be overridden
        and return a Q() expression."""

    def get(self, request, query):
        # try:
        #     q = self.generate_q_expression(query)
        #     search = self.document_class.search().query(q).sort("-publish_date")
        #     response = search.execute()
        #
        #     print(f"Found {response.hits.total.value} hit(s) for query: '{query}'")
        #
        #     results = self.paginate_queryset(response, request, view=self)
        #     serializer = self.serializer_class(results, many=True)
        #     return self.get_paginated_response(serializer.data)
        # except Exception as e:
        #     return HttpResponse(e, status=500)

        # Generate the query expression
        # q = self.generate_q_expression(query)
        #
        # # Create the search object
        # search = self.document_class.search().query(q).sort("-publish_date")
        #
        # # Loop over the query parameters and apply a filter for each one
        # for field, value in request.GET.items():
        #     if field in ArticleDocumentView.filter_fields:
        #         # Get the lookup from the filter_fields in ArticleDocumentView
        #         lookup = ArticleDocumentView.filter_fields.get(field, {}).get('lookups', [])
        #
        #         # Apply the appropriate filter based on the lookup
        #         if LOOKUP_QUERY_IN in lookup:
        #             search = search.filter('terms', **{field: value.split(',')})
        #         elif LOOKUP_FILTER_RANGE in lookup:
        #             start, end = value.split(',')
        #             search = search.filter('range', **{field: {'gte': start, 'lte': end}})
        #         else:
        #             search = search.filter('term', **{field: value})
        #
        # # Execute the search and return the results
        # response = search.execute()
        #
        # results = self.paginate_queryset(response, request, view=self)
        # serializer = self.serializer_class(results, many=True)
        # return self.get_paginated_response(serializer.data)


    # TODO: check this later
        # Generate the query expression
        q = self.generate_q_expression(query)

        # Create the search object
        search = self.document_class.search().query(q).sort("-publish_date")

        # Loop over the query parameters and apply a filter for each one
        for field, value in request.GET.items():
            if field in ArticleDocumentView.search_fields:
                # Apply the appropriate filter based on the field
                if field == 'keywords':
                    search = search.filter('term', keywords=value)
                elif field == 'authors.first_name':
                    search = search.filter('nested', path='authors', query=Q('term', authors__first_name=value))
                elif field == 'authors.last_name':
                    search = search.filter('nested', path='authors', query=Q('term', authors__last_name=value))
                elif field == 'institutions.name':
                    search = search.filter('nested', path='institutions', query=Q('term', institutions__name=value))

        # Execute the search and return the results
        response = search.execute()

        results = self.paginate_queryset(response, request, view=self)
        serializer = self.serializer_class(results, many=True)
        return self.get_paginated_response(serializer.data)


# views
class SearchArticles(PaginatedElasticSearchAPIView):
    serializer_class = ArticleDocumentSerializer
    document_class = ArticleDocument

    def generate_q_expression(self, query):
        return Q(
            "bool",
            should=[
                Q("multi_match", query=query, fields=["title", "keywords", "content"], fuzziness="auto"),
                Q("nested", path="authors", query=Q("multi_match", query=query, fields=["authors.first_name", "authors.last_name"], fuzziness="auto")),
                Q("nested", path="institutions", query=Q("multi_match", query=query, fields=["institutions.name"], fuzziness="auto"))
            ]
        )
