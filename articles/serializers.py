from rest_framework import serializers
from django_elasticsearch_dsl_drf.serializers import DocumentSerializer

from articles.documents import ArticleDocument


class ArticleDocumentSerializer(DocumentSerializer):
    keywords = serializers.ListField(child=serializers.CharField())
    class Meta(object):
        document = ArticleDocument
        fields = "__all__"
