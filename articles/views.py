from core.settings import DOCUMENTS_ROOT
from django.http import FileResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import HttpResponse as HTTPResponse

from django.core.files.storage import default_storage
import gdown
import pypdf

# ========================= Articles upload views =========================
@api_view(['POST'])
def test_file_upload_type(request):
    # use pypdf to check if the file is a pdf
    # if not pdfReader.isEncrypted: return Response("File is not a PDF", status=status.HTTP_400_BAD_REQUEST)
    file = request.FILES.get('articles')
    try:
        pypdf.PdfReader(file)
    except:
        return Response("File is not a PDF", status=status.HTTP_400_BAD_REQUEST)
    print(file.name)
    return Response(f'file uploaded!', status=status.HTTP_201_CREATED)

@api_view(['GET'])
def get_file(request, filename):
    file = open(DOCUMENTS_ROOT+filename+'.pdf', 'rb')
    return HTTPResponse(file.read(), content_type='application/pdf',status=status.HTTP_200_OK)

@api_view(['POST'])
def upload_file(request): 

    # Extracting data
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
            # check if the file is an actual pdf using pyPDF
            try:
                pypdf.PdfReader(file)
            except:
                continue
            # if not pdfReader.isEncrypted: return Response("File is not a PDF", status=status.HTTP_400_BAD_REQUEST)

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
      
# ========================= ElasticSearch views =========================
from django_elasticsearch_dsl_drf.constants import (
    LOOKUP_FILTER_RANGE,
    LOOKUP_QUERY_GTE,
    LOOKUP_QUERY_IN,
    SUGGESTER_COMPLETION,
    LOOKUP_QUERY_LTE, LOOKUP_FILTER_TERM, LOOKUP_FILTER_TERMS, LOOKUP_FILTER_PREFIX, LOOKUP_FILTER_WILDCARD,
    LOOKUP_QUERY_EXCLUDE, LOOKUP_QUERY_ISNULL,
)

from django_elasticsearch_dsl_drf.filter_backends import (
    DefaultOrderingFilterBackend,
    FacetedSearchFilterBackend,
    FilteringFilterBackend,
    CompoundSearchFilterBackend,
    SuggesterFilterBackend, NestedFilteringFilterBackend, OrderingFilterBackend,
)
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet
from articles.documents import ArticleDocument
from articles.serializers import ArticleDocumentSerializer


class ArticleDocumentView(DocumentViewSet):
    document = ArticleDocument
    serializer_class = ArticleDocumentSerializer
    ordering = ('-publish_date',)

    filter_backends = [
        DefaultOrderingFilterBackend,
        OrderingFilterBackend,
        FacetedSearchFilterBackend,
        FilteringFilterBackend,
        CompoundSearchFilterBackend,
        SuggesterFilterBackend,
        NestedFilteringFilterBackend
    ]

    search_fields = {
        'title': {'fuzziness': 'AUTO'},
        'keywords': {'fuzziness': 'AUTO'},
        'content': None,
        'summary': {'fuzziness': 'AUTO'},
    }

    search_nested_fields = {
        'authors': {
            'path': 'authors',
            'fields': {
                'first_name': {'fuzziness': 'AUTO'},
                'last_name': {'fuzziness': 'AUTO'},
            },
        },
        'institutions': {
            'path': 'institutions',
            'fields': {
                'name': {'fuzziness': 'AUTO'},
            },
        },
    }

    filter_fields = {
        'keywords': {'field': 'keywords', 'lookups': [LOOKUP_QUERY_IN]},
        # 'author_first_name': {'field': 'authors.first_name', 'lookups': [LOOKUP_QUERY_IN]},
        # 'author_last_name': {'field': 'authors.last_name', 'lookups': [LOOKUP_QUERY_IN]},
        # 'institution_name': {'field': 'institutions.name', 'lookups': [LOOKUP_QUERY_IN]},
        'publish_date': {'field': 'publish_date', 'lookups': [LOOKUP_FILTER_RANGE, LOOKUP_QUERY_GTE, LOOKUP_QUERY_LTE]},
    }

    nested_filter_fields = {
        'author_first_name': {
            'field': 'authors.first_name.raw',
            'path': 'authors',
            'lookups': [
                LOOKUP_FILTER_TERM,
                LOOKUP_FILTER_TERMS,
                LOOKUP_FILTER_PREFIX,
                LOOKUP_FILTER_WILDCARD,
                LOOKUP_QUERY_EXCLUDE,
                LOOKUP_QUERY_ISNULL,
            ],
        },
        'author_last_name': {
            'field': 'authors.last_name.raw',
            'path': 'authors',
            'lookups': [
                LOOKUP_FILTER_TERM,
                LOOKUP_FILTER_TERMS,
                LOOKUP_FILTER_PREFIX,
                LOOKUP_FILTER_WILDCARD,
                LOOKUP_QUERY_EXCLUDE,
                LOOKUP_QUERY_ISNULL,
            ],
        },
        'institution_name': {
            'field': 'institutions.name.raw',
            'path': 'institutions',
            'lookups': [
                LOOKUP_FILTER_TERM,
                LOOKUP_FILTER_TERMS,
                LOOKUP_FILTER_PREFIX,
                LOOKUP_FILTER_WILDCARD,
                LOOKUP_QUERY_EXCLUDE,
                LOOKUP_QUERY_ISNULL,
            ],
        },
    }


    faceted_search_fields = {
        'keywords': {
            'field': 'keywords',
            'enabled': True,
        },
        #TODO: fix
        # doesn't work well with the textFields
        # 'institutions': {
        #     'field': 'institutions.name.raw',
        #     'enabled': True,
        # },
        # 'authors': {
        #     'field': 'authors.last_name',
        #     'enabled': True,
        # },
    }
    ordering_fields = {
        'publish_date': 'publish_date'
    }

    suggester_fields = {
        'title_suggest': {
            'field': 'title.suggest',
            'suggesters': [
                SUGGESTER_COMPLETION,
            ],
        },
        'authors_first_name_suggest': {
            'field': 'authors.first_name.suggest',
            'suggesters': [
                SUGGESTER_COMPLETION,
            ],
        },
        'authors_last_name_suggest': {
            'field': 'authors.last_name.suggest',
            'suggesters': [
                SUGGESTER_COMPLETION,
            ],
        },
        'institution_name_suggest': {
            'field': 'institution.name.suggest',
            'suggesters': [
                SUGGESTER_COMPLETION,
            ],
        },
        'content_suggest': {
            'field': 'content.suggest',
            'suggesters': [
                SUGGESTER_COMPLETION,
            ],
        },
        'summary_suggest': {
            'field': 'summary.suggest',
            'suggesters': [
                SUGGESTER_COMPLETION,
            ],
        },
    }
