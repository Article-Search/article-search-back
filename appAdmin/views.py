from django.shortcuts import render
from user_auth.models import User
from user_auth.serializer import UserSerializer
from user_auth.decorators import role_required
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password
from django.http import Http404

#Create your views here.


@api_view(['GET','POST'])
@role_required(['moderator'])
def Create_List_Mod(request):
        if request.method=='GET':
            moderators=User.objects.filter(role=1)
            serializer=UserSerializer(moderators,many=True)
            return Response(serializer.data)
        elif request.method=='POST':
            print(f"Received data: {request.data}")
            name = request.data.get('name')
            email = request.data.get('email')
            password = request.data.get('password')       
            print(f"Extracted data: name={name}, email={email}, password={password}")
            request_data = {
                    'name': name,
                    'email': email,
                    'password': make_password(password),
                    'role': 'Mod',  # Set the role automatically
                 }
            print(request_data)
            serializer = UserSerializer(data=request_data)
            if serializer.is_valid(): 
                serializer.save()
                return Response(serializer.data,status=status.HTTP_201_CREATED)
            return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@role_required(['moderator'])
def Pickone_Modify_Delete_Mod(request, pk):
    try:
        moderator = User.objects.filter(role='Mod').get(pk=pk)
    except User.DoesNotExist:
        raise Http404

    if request.method == 'GET':
        serializer = UserSerializer(moderator)
        return Response(serializer.data)

    elif request.method == 'PUT':
        name = request.data.get('name')
        email = request.data.get('email')
        password = request.data.get('password')

        request_data = {
            'name': name,
            'email': email,
            'password': make_password(password),#reja3ha set_password
            'role': 'Mod',
        }

        serializer = UserSerializer(moderator, data=request_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        moderator.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)      