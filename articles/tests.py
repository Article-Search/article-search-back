import pytest
from django.urls import reverse
from core.settings import DOCUMENTS_ROOT
from django.core.files.uploadedfile import SimpleUploadedFile

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
def files_names():
    return ["article1.pdf", "article2.pdf", "article3.pdf"]

@pytest.fixture
def folder_name():
    return "articles_folder"

# @pytest.mark.skip
def test_one_input_file_upload(client, file_name):
    endpoint = reverse('file_upload')
    filepath = f"articles/tests_assets/{file_name}"

    # check if the temp file already exists, and delete it if yes
    if(os.path.exists(DOCUMENTS_ROOT + file_name)):
        os.remove(DOCUMENTS_ROOT + file_name) 

    file = open(filepath, 'rb')
    pdf = SimpleUploadedFile(name=file_name, content=file.read(), content_type='multipart/form-data')

    response = client.post(endpoint, {'articles': pdf})

    assert response.status_code == 201

    # remove the created pdf file
    os.remove(DOCUMENTS_ROOT + file_name) 

# @pytest.mark.skip
def test_multiple_input_files_upload(client, files_names):
    endpoint = reverse('file_upload')


    # check if the temp files already exists, and delete it if yes
    for name in files_names:
        if(os.path.exists(DOCUMENTS_ROOT + name)):
            os.remove(DOCUMENTS_ROOT + name) 

    # create a list of files
    files_list = []
    for name in files_names:
        filepath = f"articles/tests_assets/{name}"
        file = open(filepath, 'rb')
        pdf = SimpleUploadedFile(name=name, content=file.read(), content_type='multipart/form-data')
        files_list.append(pdf)

    # upload the files
    response = client.post(endpoint, {'articles': files_list})

    # assert the response code
    assert response.status_code == 201

    # remove the created pdf files
    for name in files_names:
        os.remove(DOCUMENTS_ROOT + name) 

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
