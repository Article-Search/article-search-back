from user_auth.models import User
from user_auth.serializer import UserSerializer
from articles.models import Article
from articles.serializers import ArticleSerializer
from .models import Favorite
from .serializer import FavoriteSerializer

from user_auth.decorators import role_required
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
from django.http import JsonResponse


@api_view(['GET','POST'])
# @role_required(['admin'])
def add_list_favorites(request):
    if request.method=='GET':
        print("i'm Get")
        #not finished

    elif request.method=='POST':
        print("i'm Post")
        user = request.user
        data = request.data

        try:
            article_id = data['article_id']
            article = get_object_or_404(Article, id=article_id)
        except KeyError:
            return Response({'error': 'article_id is required'}, status=status.HTTP_400_BAD_REQUEST)


    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['GET','DELETE'])
# @role_required(['user'])
def pickone_delete_favorite(request, article_id):
    user = request.user

    if request.method == 'GET':
        print("i'm Get")
        # not finished

    elif request.method == 'DELETE':
        print("i'm Delete")
        favorite = get_object_or_404(Favorite, user=user)
        article = get_object_or_404(Article, id=article_id)
        favorite.articles.remove(article)

        return Response({'status': 'Article removed from favorites successfully'})

        
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
