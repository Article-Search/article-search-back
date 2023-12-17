from django_elasticsearch_dsl_drf.constants import (
    LOOKUP_FILTER_RANGE,
    LOOKUP_QUERY_GTE,
    LOOKUP_QUERY_IN,
    SUGGESTER_COMPLETION,
)

from django_elasticsearch_dsl_drf.filter_backends import (
    DefaultOrderingFilterBackend,
    FacetedSearchFilterBackend,
    FilteringFilterBackend,
    SearchFilterBackend,
    SuggesterFilterBackend,
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
        FacetedSearchFilterBackend,
        FilteringFilterBackend,
        SearchFilterBackend,
        SuggesterFilterBackend,
    ]

    search_fields = (
        'title',
        'authors',
        'keywords',
        'integral_text'
        'institutions',
    )
    filter_fields = {
        'keywords': {'field': 'keywords', 'lookups': [LOOKUP_QUERY_IN]},
        'authors_first_name': {'field': 'authors.first_name', 'lookups': [LOOKUP_QUERY_IN]},
        'authors_last_name': {'field': 'authors.last_name', 'lookups': [LOOKUP_QUERY_IN]},
        'institution_name': {'field': 'institution.name', 'lookups': [LOOKUP_QUERY_IN]},
        'publish_date': {'field': 'publish_date', 'lookups': [LOOKUP_FILTER_RANGE]},
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
    }
    faceted_search_fields = {
        'keywords': {
            'field': 'keywords',
            'enabled': True,
        },
    }
