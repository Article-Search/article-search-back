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
        favorites = Favorite.objects.all()
        serializer = FavoriteSerializer(favorites, many=True)
        return Response(serializer.data)
        #not finished

    elif request.method=='POST':
        print("i'm Post")
        serializer = FavoriteSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','DELETE'])
# @role_required(['user'])
def pickone_delete_favorite(request, pk):
    try:
        favorite = Favorite.objects.get(pk=pk)
    except Favorite.DoesNotExist:
        return Response({'message': 'Favorite not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = FavoriteSerializer(favorite)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

        
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
