from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializer import UserSerializer
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import authentication_classes, permission_classes
from .decorators import role_required

# Create your views here.

@api_view(['POST'])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        role =3
        serializer.save(role=role)#here the password is hashed and role is set because of the create_user function in the manager that is called in the create function in the serializer
        #get user with hashed password
        user = User.objects.get(email=request.data['email'])
        token = Token.objects.create(user=user)
        return Response({'token': token.key, 'user': serializer.data})
    return Response(serializer.errors, status=status.HTTP_200_OK)

@api_view(['POST'])
def login(request):
    email = request.data['email']
    password = request.data['password']
    try:
        user = User.objects.get(email=email)
        if user.check_password(password):
            token = Token.objects.get(user=user)
            return Response({'token': token.key, 'user': UserSerializer(user).data})
        else:
            return Response({'error': 'Wrong password'}, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({'error': 'User does not exist'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def logout(request):
    request.user.auth_token.delete()
    return Response(status=status.HTTP_200_OK)

#this one is for test purpose test_token
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def test_token(request):
    return Response({'message': 'You are authenticated'}, status=status.HTTP_200_OK)

#create test_admin and test_user and test_moderator for testing the role_required decorator
@api_view(['GET'])
@role_required(['admin'])
def test_admin(request):
    return Response({'message': 'You are admin'}, status=status.HTTP_200_OK)

@api_view(['GET'])
@role_required(['moderator'])
def test_moderator(request):
    return Response({'message': 'You are moderator'}, status=status.HTTP_200_OK)

@api_view(['GET'])
@role_required(['user'])
def test_user(request):
    return Response({'message': 'You are user'}, status=status.HTTP_200_OK)

# add test_moderator_admin for testing the role_required decorator
@api_view(['GET'])
@role_required(['moderator','admin'])
def test_moderator_admin(request):
    return Response({'message': 'You are moderator or admin'}, status=status.HTTP_200_OK)