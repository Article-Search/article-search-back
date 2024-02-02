# user_auth/serializers.py
from rest_framework import serializers
from .models import Favorite

class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = '__all__'



# from rest_framework import serializers
# from .models import Favorite
# from articles.serializers import ArticleSerializer

# class FavoriteSerializer(serializers.ModelSerializer):
#     articles = ArticleSerializer(many=True)

#     class Meta:
#         model = Favorite
#         fields = '__all__'