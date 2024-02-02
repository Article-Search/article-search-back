from rest_framework import serializers
from .models import Favorite
from articles.models import Article

class FavoriteSerializer(serializers.ModelSerializer):
    articles = serializers.PrimaryKeyRelatedField(queryset=Article.objects.all(), many=True)

    class Meta:
        model = Favorite
        fields = '__all__'