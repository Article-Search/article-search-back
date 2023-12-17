import pytest
from django.urls import reverse
from core.settings import DOCUMENTS_ROOT

import os

# Create your tests here.
def testSayHello(client):
    url = reverse('articles_home')
    response = client.get(url)
    assert response.status_code == 200

def testFileUpload(client):
    filename = "pdf1.pdf"
    filepath = f"articles/tests_assets/{filename}"

    # check if the temp file already exists, and delete it if yes
    if(os.path.exists(DOCUMENTS_ROOT + filename)):
        os.remove(DOCUMENTS_ROOT + filename) 

    url = reverse('file_upload')
    pdf = open(filepath, "rb")

    response = client.post(url, {"articles": pdf}, format="multipart")

    assert response.status_code == 201
