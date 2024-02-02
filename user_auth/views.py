from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializer import UserSerializer
# from rest_framework.authtoken.models import Token
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import authentication_classes, permission_classes
from .decorators import role_required
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from django.core.exceptions import ObjectDoesNotExist
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
# Create your views here.


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['role'] = user.role 

        return token
        def validate(self, attrs):
            data = super().validate(attrs)

            refresh = self.get_token(self.user)
            data['refresh'] = str(refresh)
            data['access'] = str(refresh.access_token)

            return data

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        role = 3
        serializer.save(role=role)
        user = User.objects.get(email=request.data['email'])
        refresh = RefreshToken.for_user(user)
        access = CustomTokenObtainPairSerializer.get_token(user)
        return Response({
            'refresh': str(refresh),
            'access': str(access),
            'user': serializer.data
        })
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    email = request.data['email']
    password = request.data['password']
    try:
        user = User.objects.get(email=email)
        if user.check_password(password):
            refresh = CustomTokenObtainPairSerializer.get_token(user)
            access = str(refresh.access_token)
            return Response({
                'refresh': str(refresh),
                'access': str(access),
                'user': UserSerializer(user).data
            })
        else:
            return Response({'error': 'Wrong password'}, status=status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        return Response({'error': 'User does not exist'}, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['GET'])
# def logout(request):
#     request.user.auth_token.delete()
#     return Response(status=status.HTTP_200_OK)

# #this one is for test purpose test_token
# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @authentication_classes([TokenAuthentication])
# def test_token(request):
#     return Response({'message': 'You are authenticated'}, status=status.HTTP_200_OK)

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
    print("request")
    return Response({'message': 'You are user'}, status=status.HTTP_200_OK)

@api_view(['GET'])
@role_required(['moderator','admin'])
def test_moderator_admin(request):
    return Response({'message': 'You are moderator or admin'}, status=status.HTTP_200_OK)

#reset password view
@api_view(['POST'])
@role_required(['user','admin','moderator'])
def reset_password(request):
    email = request.data['email']
    #check if the email is of the user that is logged in
    if request.user.email != email:
        return Response({'error': 'You are not allowed to reset password for this user'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        user = User.objects.get(email=email)
        user.set_password(request.data['password'])
        user.save()
        return Response({'message': 'Password reset successfully'}, status=status.HTTP_200_OK)
    except ObjectDoesNotExist:
        return Response({'error': 'User does not exist'}, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['POST'])
@permission_classes([AllowAny])
def custom_token_refresh(request):
    serializer = TokenRefreshSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    return Response(serializer.validated_data, status=status.HTTP_200_OK)