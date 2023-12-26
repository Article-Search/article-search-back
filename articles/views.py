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
    faceted_search_fields = {
        'keywords': {
            'field': 'keywords',
            'enabled': True,
        },
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
