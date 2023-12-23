from django.http import HttpResponse
from django.http.response import json
import pytest
from core.settings import DOCUMENTS_ROOT


from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from django.core.files.storage import default_storage
import gdown

# Create your views here.
@api_view(['GET'])
def hello(request):
    return Response("Welcome to articles!", status=status.HTTP_200_OK)

@api_view(['POST'])
def upload_file(request):  # use APIview or function based view or any view u want
    # Extracting data

    try:
        print(f"Here I shoot a test! {request.data}")
    except Exception as e:
        print(e)
    body = request.data
    url = body.get('url')
    is_directory = body.get('is-directory')

    if url:
        name = body.get('name')
        if not name: return Response("Name should be specificed", status=status.HTTP_400_BAD_REQUEST)

        return upload_file_with_url(name, url, is_directory)

    else:
        # the upload is through file input

        # for multiple file
        files = request.FILES.getlist('articles')
        print(files)
        print(request.data)
        if not len(files): return Response("No files provided. Enter either a file(s) or a URL", status=status.HTTP_400_BAD_REQUEST)

        for file in files:
            print(file.name)
            # Do what ever you want with it

            default_storage.save(DOCUMENTS_ROOT+file.name, file)

        return Response(f'file(s) uploaded!', status=status.HTTP_201_CREATED)

def upload_file_with_url(name, url, is_directory=False):
    output = DOCUMENTS_ROOT + name

    if is_directory:
        # example URL: url = "https://drive.google.com/drive/folders/15uNXeRBIhVvZJIhL4yTw4IsStMhUaaxl"
        gdown.download_folder(url, quiet=True, output=output, use_cookies=False)

        return Response(f'file(s) uploaded!', status=status.HTTP_201_CREATED)

    else:
        # example URL: url = "https://drive.google.com/file/d/0B9P1L--7Wd2vNm9zMTJWOGxobkU/view?usp=sharing"
        gdown.download(url=url, output=output, quiet=False, fuzzy=True)

        return Response(f'file uploaded!', status=status.HTTP_201_CREATED)
