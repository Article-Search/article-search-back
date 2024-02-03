from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from user_auth.models import User
from user_auth.serializer import UserSerializer
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Favorite
from articles.models import Article
from django.core import serializers
import json



@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user(request):
    user = request.user
    serializer = UserSerializer(user, data=request.data, partial=True)  # set partial=True to update a data partially
    if serializer.is_valid():
        user.first_name = serializer.validated_data.get('first_name', user.first_name)
        user.last_name = serializer.validated_data.get('last_name', user.last_name)
        user.email = serializer.validated_data.get('email', user.email)
        user.save()
        return Response(UserSerializer(user).data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_favorites(request):
    user = request.user
    # get article id from request body
    article_id = request.data.get('article_id')
    article = get_object_or_404(Article, pk=article_id)

    favorite, created = Favorite.objects.get_or_create(user=user)

    if article not in favorite.articles.all():
        favorite.articles.add(article)

    return JsonResponse({'message': 'Article added to favorites'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_favorites(request):
    user = request.user
    favorite = get_object_or_404(Favorite, user=user)

    articles = list(favorite.articles.values('pk', 'elasticsearch_id'))

    return JsonResponse({'articles': articles})



@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_from_favorites(request, article_id):
    user = request.user
    article = get_object_or_404(Article, pk=article_id)
    favorite = get_object_or_404(Favorite, user=user)

    if article in favorite.articles.all():
        favorite.articles.remove(article)

    return JsonResponse({'message': 'Article removed from favorites'})