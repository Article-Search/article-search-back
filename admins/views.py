from user_auth.models import User
from user_auth.serializer import UserSerializer
from user_auth.decorators import role_required
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password

@api_view(['GET','POST'])
@role_required(['admin'])
def create_list_moderators(request):
    if request.method=='GET':
        moderators=User.objects.filter(role=2)
        serializer=UserSerializer(moderators,many=True)
        return Response({'users': serializer.data}, status=status.HTTP_200_OK)

    elif request.method=='POST':

        # Extract the data
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        first_name=request.data.get('first_name')
        last_name=request.data.get('last_name')       

        request_data = {
            'username': username,
            'email': email,
            'password': make_password(password),
            'role': 2,  # Set the role automatically
            'first_name':first_name,
            'last_name':last_name,
        }

        serializer = UserSerializer(data=request_data)
        if serializer.is_valid(): 
            serializer.save()
            return Response({'user': serializer.data},status=status.HTTP_201_CREATED)

        print(serializer.errors)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['GET', 'PUT', 'DELETE'])
@role_required(['admin'])
def pickone_modify_delete_moderator(request, id):
    print(f"id: {id}")
    moderator = None

    try:
        moderator = User.objects.filter(role=2).get(pk=id)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserSerializer(moderator)
        return Response({'user': serializer.data})

    elif request.method == 'PUT':
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        first_name=request.data.get('first_name')
        last_name=request.data.get('last_name')  
        request_data = {
            'username': username,
            'email': email,
            'password': make_password(password),#reja3ha set_password
            'role': 2,
            'first_name':first_name,
            'last_name':last_name,            
        }

        serializer = UserSerializer(moderator, data=request_data)
        if serializer.is_valid():
            serializer.save()
            return Response({'user': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        moderator.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
