from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
from rest_framework import serializers
from articles.documents import ArticleDocument
from .models import Article



class ArticleDocumentSerializer(DocumentSerializer):
    class Meta:
        document = ArticleDocument
        fields = "__all__"

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'