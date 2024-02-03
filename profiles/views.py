from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from user_auth.models import User
from user_auth.serializer import UserSerializer

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