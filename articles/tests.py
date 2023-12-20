import pytest
from django.urls import reverse
from core.settings import DOCUMENTS_ROOT

import os

@pytest.fixture
def drive_directory_url():
    return "https://drive.google.com/drive/folders/10pzgHpHbTrOBRQ-m91MKGf6anYjgwQHG?usp=drive_link"

@pytest.fixture
def drive_file_url():
    return "https://drive.google.com/file/d/1J5FxS2e1Iv_5enmqFsXwAZR_S2j5whI9/view?usp=drive_link"

@pytest.fixture
def file_name():
    return "article.pdf"

@pytest.fixture
def folder_name():
    return "articles_folder"

# Create your tests here.
def test_say_hello(client):
    endpoint = reverse('articles_home')
    
    response = client.get(endpoint)

    assert response.status_code == 200

@pytest.mark.skip
def test_one_input_file_upload(client, file_name):
    endpoint = reverse('file_upload')

    file_name = "pdf1.pdf"
    filepath = f"articles/tests_assets/{file_name}"

    # check if the temp file already exists, and delete it if yes
    if(os.path.exists(DOCUMENTS_ROOT + file_name)):
        os.remove(DOCUMENTS_ROOT + file_name) 

    pdf = open(filepath, "rb")

    headers = {
        # 'Content-Type': 'application/pdf'
        'Content-Type': 'multipart/form-data; boundary=---------------------------974767299852498929531610575'
    }

    # response = client.post(endpoint, {"articles": pdf}, headers=headers, format="multipart")
    response = client.post(endpoint, {"articles": pdf}, headers=headers)

    assert response.status_code == 201

def test_multiple_input_files_upload(client, file_name):
    pass

@pytest.mark.skip
def test_one_google_drive_file_upload(client, file_name, drive_file_url):
    endpoint = reverse('file_upload')

    response = client.post(endpoint, {"url": drive_file_url, "name": file_name, "is-directoy": False})

    assert response.status_code == 201

@pytest.mark.skip
def test_one_google_drive_folder_upload(client, folder_name, drive_directory_url):
    endpoint = reverse('file_upload')

    response = client.post(endpoint, {"url": drive_directory_url, "name": file_name, "is-directoy": True})

    assert response.status_code == 201
