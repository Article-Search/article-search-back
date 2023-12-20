import abc

from django.http import HttpResponse
from elasticsearch_dsl import Q
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from articles.documents import ArticleDocument
from articles.serializers import ArticleDocumentSerializer


class PaginatedElasticSearchAPIView(APIView, LimitOffsetPagination):
    serializer_class = None
    document_class = None

    @abc.abstractmethod
    def generate_q_expression(self, query):
        """This method should be overridden
        and return a Q() expression."""

    def get(self, request, query):
        try:
            # TODO: changed this here
            q = self.generate_q_expression(query)
            search = self.document_class.search().query(q)
            return Response(self.serializer_class(search.to_queryset(), many=True).data)
        except Exception as e:
            return HttpResponse(e, status=500)


# views
class SearchArticles(PaginatedElasticSearchAPIView):
    serializer_class = ArticleDocumentSerializer
    document_class = ArticleDocument

    def generate_q_expression(self, query):
        return Q(
            "multi_match", query=query,
            fields=[
                "title",
                "authors",
                "keywords",
                "content",
                "institutions"
            ], fuzziness="auto")
