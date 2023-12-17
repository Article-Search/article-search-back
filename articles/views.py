from django.http import HttpResponse
from django.http.response import json
from rest_framework import serializers

from django.core.files.storage import default_storage
import gdown

# Create your views here.
def hello(request):
    return HttpResponse("Welcome to articles!")

def upload_file(request):  # use APIview or function based view or any view u want
    # for single file
    # file = request.FILES["article"]
    # print(file.name)
    # Do what ever you want with it

    # return upload_file_with_url(request)
    # for multiple file
    files = request.FILES.getlist('articles')

    for file in files:
        print(file.name)
        # Do what ever you want with it

        default_storage.save(f"temp/files/{file.name}", file)
        # try:
        #     with open(f"temp/files/{file.name}", "wb") as buffer:
        #         shutil.copyfileobj(.file, buffer)
        # finally:
        #     upload_file.file.close()

    return HttpResponse(f'file(s) uploaded!', status=201)

def upload_file_with_url(request):
    print(request.body)
    url = json.loads(request.body)['url']
    print(url)

    output = 'temp/files/pdf1.pdf'
    gdown.download(url=url, output=output, quiet=False, fuzzy=True)

    return HttpResponse(f'file(s) uploaded!')
